from typing import Generator, Optional, Iterable
from openai import OpenAI, Stream
import logging
import json
import os

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class QuizGenerator:
    EXAMPLE_RESPONSE = json.dumps(
        {
            "question_id": 1,
            "question": "Who was the first emperor of Rome?",
            "A": "Julius Caesar",
            "B": "Augustus",
            "C": "Constantine",
            "answer": "B",
            "explanation": (
                "Augustus, originally Octavian, "
                "was the first to hold the title of Roman Emperor. "
                "Julius Caesar, while pivotal, never held the emperor title."
            ),
            "wikipedia": r"https://en.wikipedia.org/wiki/Augustus",
        }
    )

    @classmethod
    def get_api_key_from_env(cls) -> str:
        """Retrieves the OpenAI API key from environment variables.

        Returns:
            str: The API key from the environment variable OPENAI_API_KEY.

        Raises:
            ValueError: If the environment variable is not set or empty.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "Environment variable OPENAI_API_KEY is not set. "
                "Please ensure it's set and try again."
            )
        return api_key

    def __init__(self, api_key: Optional[str] = None):
        """
        Initializes the QuizGenerator by setting up the OpenAI client with the API key.
        If `api_key` is not provided, it is retrieved from the environment
        using `get_api_key_from_env`.

        Args:
            api_key (str, optional): The OpenAI API key to use. Defaults to None.
        """
        if api_key is None:
            api_key = self.get_api_key_from_env()

        self.client = OpenAI(api_key=api_key)

    def generate_quiz(
        self, topic: str, difficulty: str, n_questions: int = 10
    ) -> Generator[str, None, None]:
        """
        Generate a quiz based on the provided topic and difficulty using OpenAI API.

        Parameters:
        - topic (str): The subject for the quiz, e.g., 'Roman History'.
        - difficulty (str): The desired difficulty of the quiz e.g., 'Easy', 'Medium'.
        - n_questions (int, optional): Number of questions required. Defaults to 10.

        Returns:
        - str: JSON-formatted quiz questions. If an error occurs, an empty string is returned.

        This method coordinates the creation of the role for the OpenAI API,
        the generation of the response, and the cleaning of the response.
        """
        role = self._create_role(topic, difficulty, n_questions)
        logger.info(f"Role content for OpenAI API: {role}")
        openai_stream = self._create_openai_stream(role)
        response_generator = self._create_question_generator(openai_stream)

        return response_generator

    def _create_role(self, topic: str, difficulty: str, n_questions: int) -> str:
        """
        Creates the role string that will be sent to the OpenAI API to generate the quiz.

        Parameters:
        - topic (str): The subject for the quiz.
        - difficulty (str): The desired difficulty of the quiz.
        - n_questions (int): Number of questions required.

        Returns:
        - str: The role string to be sent to the OpenAI API.

        This method structures the prompt for the OpenAI API to ensure consistent and correct responses.
        """
        return (
            f"You are an AI to generate quiz questions. "
            f"You will be given a topic e.g. Roman History with a difficulty of Normal. "
            f"Give {str(n_questions)} responses in a json format such as: {self.EXAMPLE_RESPONSE}. "
            f"Your task is to generate similar responses for {topic} "
            f"with the difficulty of {difficulty}. "
            f"ENSURE THESE ARE CORRECT. DO NOT INCLUDE INCORRECT ANSWERS! "
            f"DO NOT PREFIX THE RESPONSE WITH ANYTHING EXCEPT THE RAW JSON! "
            f"Return each question on a new line. "
        )

    def _create_openai_stream(self, role: str) -> Stream:
        """
        Creates the stream from the OpenAI API based on the given role.
        Exceptions are not caught here so that errors are visible in tests.

        Parameters:
        - role (str): The role string to be sent to the OpenAI API.

        Returns:
        - str: The raw response from the OpenAI API.
        """
        return self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "user", "content": role}],
            stream=True,
        )

    def _create_question_generator(
        self, openai_stream: Stream
    ) -> Generator[str, None, None]:
        """Parses streamed data chunks from OpenAI into complete JSON objects and yields them in SSE format.

        Accumulates data in a buffer and attempts to parse complete JSON objects. If successful,
        the JSON object is yielded as a string and the buffer is cleared for the next object.
        Ignores empty chunks and continues buffering if the JSON is incomplete.

        Similar-ish SSE Fast API blog: https://medium.com/@nandagopal05/server-sent-events-with-python-fastapi-f1960e0c8e4b
        Helpful SO that says about the SSE format of data: {your-json}: https://stackoverflow.com/a/49486869/11902832

        Args:
            openai_stream (Stream): Stream from OpenAI's api

        Yields:
            str: Complete JSON object of a quiz question in string representation.
        """
        buffer = ""
        for chunk in openai_stream:
            chunk_contents = chunk.choices[0].delta.content

            # Ignore empty chunks.
            if chunk_contents is None:
                logger.debug("Chunk was empty!")
                continue

            buffer += chunk_contents  # Append new data to buffer
            result = self.validate_and_parse_json(buffer)

            # If the JSON is incomplete, wait for more data.
            if result is None:
                logger.debug("JSON is incomplete, waiting for more data...")
                continue

            # If the JSON is complete, yield it and clear the buffer.
            yield self._format_sse(result)
            buffer = ""  # Clear buffer on successful parse.

        logger.info("Finished stream!")

    @staticmethod
    def _format_sse(json_obj: dict) -> str:
        """
        Formats a JSON object as a Server-Sent Event (SSE) string.
        """
        return f"data: {json.dumps(json_obj)}\n\n"

    @staticmethod
    def validate_and_parse_json(s: str) -> Optional[dict]:
        """
        Helper method to validate and parse the provided string as JSON.
        Returns the parsed dict if s is valid JSON, otherwise returns None if the JSON is incomplete.

        Parameters:
        - s (str): The string to check.

        Returns:
        - dict: The parsed JSON object, or None if the JSON is incomplete.
        """
        try:
            return json.loads(s)
        except json.JSONDecodeError as e:
            logger.debug(f"Incomplete JSON '{s}': {e.msg} at pos {e.pos}")
            return None

    @staticmethod
    def print_quiz(generator: Generator[str, None, None]):
        """Helper function to iterate through and print the results from the question generator.

        Args:
            generator (Generator[str, None, None]): Generator producing quiz questions as SSE formatted strings.
        """
        try:
            for idx, question in enumerate(generator, start=1):
                logger.info(f"Item {idx}: {question}")
        except Exception as e:
            logger.error(f"Error during quiz generation: {e}")


if __name__ == "__main__":
    # Set logger level to DEBUG if running this file to test
    logger.setLevel(logging.DEBUG)

    quiz_generator = QuizGenerator()
    topic = "Crested Gecko"
    difficulty = "Medium"
    generator = quiz_generator.generate_quiz(topic, difficulty, 2)
    logger.info(generator)
    QuizGenerator.print_quiz(generator)

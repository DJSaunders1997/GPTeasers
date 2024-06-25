# https://github.com/openai/openai-python
from typing import Generator
from openai import OpenAI, Stream
import logging
import json
import os

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class QuizGenerator:
    # TODO: Implement a method of getting the quiz in the old format, even if it takes a while.
    EXAMPLE_RESPONSE = json.dumps({
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
    })

    def __init__(self):
        """
        Initializes the QuizGenerator by setting up the OpenAI client with the API key from environment variables.
        Raises an error if the API key is not set.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "Environment variable OPENAI_API_KEY is not set. "
                "Please ensure it's set and try again."
            )
        self.client = OpenAI(api_key=api_key)

    def generate_quiz(self, topic: str, difficulty: str, n_questions: str = "10", stream: bool = False) -> Generator[str, None, None]:
        """
        Generate a quiz based on the provided topic and difficulty using OpenAI API.
        
        Parameters:
        - topic (str): The subject for the quiz, e.g., 'Roman History'.
        - difficulty (str): The desired difficulty of the quiz e.g., 'Easy', 'Medium'.
        - n_questions (str, optional): Number of questions required. Defaults to '10'.
        - stream (bool, optional): Whether to stream the response. Defaults to False.
        
        Returns:
        - str: JSON-formatted quiz questions. If an error occurs, an empty string is returned.
        
        This method coordinates the creation of the role for the OpenAI API,
        the generation of the response, and the cleaning of the response.
        """
        role = self._create_role(topic, difficulty, n_questions)

        logging.info(f"Role content for OpenAI API: {role}")

        stream = self._create_openai_stream(role)

        response_generator = self._create_question_generator(stream)

        return response_generator

    def _create_role(self, topic: str, difficulty: str, n_questions: str) -> str:
        """
        Creates the role string that will be sent to the OpenAI API to generate the quiz.
        
        Parameters:
        - topic (str): The subject for the quiz.
        - difficulty (str): The desired difficulty of the quiz.
        - n_questions (str): Number of questions required.
        
        Returns:
        - str: The role string to be sent to the OpenAI API.
        
        This method structures the prompt for the OpenAI API to ensure consistent and correct responses.
        """
        return (
            f"You are an AI to generate quiz questions. "
            f"You will be given a topic e.g. Roman History with a difficulty of Normal. "
            f"Give {n_questions} responses in a json format such as: {self.EXAMPLE_RESPONSE}. "
            f"Your task is to generate similar responses for {topic} "
            f"with the difficulty of {difficulty}. "
            f"ENSURE THESE ARE CORRECT. DO NOT INCLUDE INCORRECT ANSWERS! "
            f"DO NOT PREFIX THE RESPONSE WITH ANYTHING EXCEPT THE RAW JSON! "
            f"Return each question on a new line. "
        )

    def _create_openai_stream(self, role: str) -> Stream:
        """
        Creates the stream from the OpenAI API based on the given role.
        
        Parameters:
        - role (str): The role string to be sent to the OpenAI API.
        
        Returns:
        - str: The raw response from the OpenAI API.
        
        This method handles the API call to OpenAI and returns the raw response.
        If an error occurs, it logs the error and returns an empty string.
        """
        try:
            openai_stream = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": role}],
                stream=True
            )
        except Exception as e:
            logging.error(f"General error when creating OpenAI stream: {e}")
        return openai_stream
            

    def _create_question_generator(self, openai_stream: Stream) -> Generator[str, None, None]:
        """Parses streamed data chunks from OpenAI into complete JSON objects and yields them.

        Accumulates data in a buffer and attempts to parse complete JSON objects. If successful,
        the JSON object is yielded as a string and the buffer is cleared for the next object.
        Ignores empty chunks and continues buffering if the JSON is incomplete.

        Similar-ish SSE Fast API blog: https://medium.com/@nandagopal05/server-sent-events-with-python-fastapi-f1960e0c8e4b
        Helpful SO that says about the SSE format of data: {your-json}: https://stackoverflow.com/a/49486869/11902832
        
        Args:
            openai_stream (Stream): Stream from OpenAI's api

        Yields:
            str: Complete JSON object of a quiz question in string representation.
        
        Raises:
            json.JSONDecodeError: If parsing fails due to malformed JSON data.
        """


        buffer = ""
        for chunk in openai_stream:
            chunk_contents = chunk.choices[0].delta.content
            # Ignore empty chunks.
            if chunk_contents is None:
                logger.info("Chunk was empty!")
                continue
            buffer += chunk_contents  # Append new data to buffer
            try:
                while buffer:
                    obj = json.loads(buffer)  # Try to parse buffer as JSON
                    logger.info(f"Successfully parsed response as JSON object! {obj}")
                    formatted_sse = f"data: {json.dumps(obj)}\n\n"  # Format as SSE
                    logger.info(f"Successfully formatted data as SSE event: {formatted_sse}")
                    yield formatted_sse  # Yield the JSON string
                    buffer = ""  # Clear buffer since JSON was successfully parsed
            except json.JSONDecodeError:
                continue  # Continue buffering if JSON is incomplete
        
        logger.info("Finished stream!")

    @staticmethod
    def print_quiz(generator: Generator[str, None, None]):
        """Helper function to iterate through and print the results from the question generator.
        
        Args:
            generator (Generator[str, None, None]): Generator producing quiz questions as SSE formatted strings.
        """
        try:
            i = 1
            for question in generator:
                logger.info(f"Item {i}: {question}")
                i += 1
        except Exception as e:
            logger.error(f"Error during quiz generation: {e}")

if __name__ == "__main__":
    quiz_generator = QuizGenerator()

    topic = "Crested Gecko"
    difficulty = "Medium"
    generator = quiz_generator.generate_quiz(topic, difficulty, "5", stream=True)
    logger.info(generator)
    
    QuizGenerator.print_quiz(generator)

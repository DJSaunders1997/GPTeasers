from typing import Generator, Optional
import logging
import json
import os

# Import the completion function from litellm (as shown in the docs example)
from litellm import completion

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class QuizGenerator:
    example_question_1 = json.dumps(
        {
            "question_id": 1,
            "question": "Who was the first emperor of Rome?",
            "A": "Julius Caesar",
            "B": "Augustus",
            "C": "Constantine",
            "answer": "B",
            "explanation": (
                "Augustus, originally Octavian, was the first to hold the title of Roman Emperor. "
                "Julius Caesar, while pivotal, never held the emperor title."
            ),
            "wikipedia": "https://en.wikipedia.org/wiki/Augustus",
        }
    )

    example_question_2 = json.dumps({
        "question_id": 2,
        "question": (
            "Which Roman Emperor is known for issuing the Edict on Maximum Prices to curb inflation, "
            "and is regarded as a pivotal figure in the transition from the Principate to the Dominate?"
        ),
        "A": "Nero",
        "B": "Diocletian",
        "C": "Marcus Aurelius",
        "answer": "B",
        "explanation": (
            "Diocletian, who reigned from 284 to 305 AD, issued the Edict on Maximum Prices in 301 AD in an effort "
            "to control rampant inflation and economic instability. His reforms marked a significant shift in the "
            "structure of Roman imperial governance."
        ),
        "wikipedia": "https://en.wikipedia.org/wiki/Diocletian",
    })

    EXAMPLE_RESPONSE = example_question_1 + "\n" + example_question_2

    @classmethod
    def check_api_key_from_env(cls) -> None:
        """Retrieves the API keys from environment variables.

        Raises:
            ValueError: If the environment variable is not set or empty.
        """

        for key in [
            "OPENAI_API_KEY",
            "GEMINI_API_KEY",
            "DEEPSEEK_API_KEY",
            "AZURE_AI_API_KEY",
            "AZURE_AI_API_BASE",
        ]:
            api_key = os.getenv(key)
            if not api_key:
                raise ValueError(
                    f"Environment variable {key} is not set."
                    "Please ensure it's set and try again."
                )

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-3.5-turbo",
    ):
        """
        Initializes the QuizGenerator.
        If `api_key` is not provided, it is retrieved from the environment.

        Args:
            api_key (str, optional): The API key to use. Defaults to None.
            model (str, optional): The model name to use. Defaults to "gpt-3.5-turbo".
        """

        self.check_api_key_from_env()

        self.model = model

    def generate_quiz(
        self, topic: str, difficulty: str, n_questions: int = 10
    ) -> Generator[str, None, None]:
        """
        Generate a quiz based on the provided topic and difficulty using litellm.

        Parameters:
            topic (str): The subject for the quiz (e.g., 'Roman History').
            difficulty (str): The desired difficulty (e.g., 'Easy', 'Medium').
            n_questions (int, optional): Number of questions required. Defaults to 10.

        Returns:
            Generator[str, None, None]: A generator yielding JSON-formatted quiz questions as SSE strings.
        """
        prompt = self._create_role(topic, difficulty, n_questions)
        logger.info(f"Prompt for LLM: {prompt}")
        llm_stream = self._create_llm_stream(prompt)
        response_generator = self._create_question_generator(llm_stream)
        return response_generator

    def _create_role(self, topic: str, difficulty: str, n_questions: int) -> str:
        """
        Creates the prompt to be sent to the LLM.

        Parameters:
            topic (str): The quiz subject.
            difficulty (str): The quiz difficulty.
            n_questions (int): Number of questions to generate.

        Returns:
            str: The prompt string.
        """
        return (
            f"You are an AI that generates quiz questions. "
            f"You will be given a topic (e.g., Roman History) with a difficulty level. "
            f"Provide {n_questions} responses in JSON format similar to this example: \n{self.EXAMPLE_RESPONSE}. "
            f"Generate similar responses for the topic '{topic}' with a difficulty of '{difficulty}'. "
            f"ENSURE THESE ARE CORRECT. DO NOT INCLUDE INCORRECT ANSWERS! "
            f"DO NOT PREFIX THE RESPONSE WITH ANYTHING EXCEPT THE RAW JSON! "
            f"Return each question on a new line."
        )

    def _create_llm_stream(self, prompt: str):
        """
        Creates a streaming response from litellm based on the given prompt.

        Parameters:
            prompt (str): The prompt string.

        Returns:
            Generator: A generator yielding streamed response chunks from the LLM.
        """
        # The completion function supports a stream flag.
        return completion(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )

    def _create_question_generator(self, llm_stream) -> Generator[str, None, None]:
        """
        Parses streamed data chunks from the LLM into complete JSON objects and yields them as SSE strings.

        Accumulates data in a buffer and attempts to parse complete JSON objects. If successful,
        the JSON object is yielded as a string and the buffer is cleared for the next object.
        Ignores empty chunks and continues buffering if the JSON is incomplete.

        Similar-ish SSE Fast API blog: https://medium.com/@nandagopal05/server-sent-events-with-python-fastapi-f1960e0c8e4b
        Helpful SO that says about the SSE format of data: {your-json}: https://stackoverflow.com/a/49486869/11902832

        Args:
            openai_stream (Stream): Stream from OpenAI's api

        Yields:
            str: A JSON object formatted as an SSE string.
        """
        buffer = ""
        for chunk in llm_stream:
            try:
                # Adjust extraction if your provider returns a different structure.
                chunk_contents = chunk.choices[0].delta.content
            except (AttributeError, IndexError, KeyError):
                logger.debug("Chunk format unexpected or chunk is empty!")
                continue

            if chunk_contents is None:
                logger.debug("Received an empty chunk; skipping...")
                continue

            buffer += chunk_contents  # Append new data to the buffer
            result = self.validate_and_parse_json(buffer)

            # If the JSON is incomplete, wait for more data.
            if result is None:
                logger.debug("JSON is incomplete, waiting for more data...")
                continue

            # If the JSON is complete, yield it and clear the buffer.
            yield self._format_sse(result)
            buffer = ""  # Clear buffer for next JSON object

        logger.info("Finished processing the stream!")

    @staticmethod
    def _format_sse(json_obj: dict) -> str:
        """
        Formats a JSON object as a Server-Sent Event (SSE) string.
        """
        return f"data: {json.dumps(json_obj)}\n\n"

    @staticmethod
    def validate_and_parse_json(s: str) -> Optional[dict]:
        """
        Validates and parses a string as JSON.

        Parameters:
            s (str): The string to parse.

        Returns:
            Optional[dict]: The parsed JSON if successful, otherwise None.
        """
        try:
            return json.loads(s)
        except json.JSONDecodeError as e:
            logger.debug(f"Incomplete JSON '{s}': {e.msg} at pos {e.pos}")
            return None

    @staticmethod
    def print_quiz(generator: Generator[str, None, None]):
        """
        Iterates through the generator and prints each quiz question.

        Parameters:
            generator (Generator[str, None, None]): Generator producing quiz questions as SSE strings.
        """
        questions = []
        try:
            for idx, question in enumerate(generator, start=1):
                logger.info(f"Item {idx}: {question}")
                questions.append(question)
            return questions
        except Exception as e:
            logger.error(f"Error during quiz generation: {e}")


if __name__ == "__main__":
    # For detailed output during testing, set the logger level to DEBUG.
    logger.setLevel(logging.DEBUG)


    # Instantiate QuizGenerator. You can change the provider and model if needed.
    suppported_models = [
        "gpt-3.5-turbo",
        "gpt-4-turbo",
        "o1-mini",
        "o3-mini",
        "gemini/gemini-pro",
        "gemini/gemini-1.5-pro-latest",
        "azure_ai/DeepSeek-R1",
    ]

    quiz_generator = QuizGenerator(model="o1-mini")

    topic = "Crested Gecko"
    difficulty = "Medium"
    generator = quiz_generator.generate_quiz(topic, difficulty, n_questions=2)
    logger.info("Starting quiz generation...")
    quiz = QuizGenerator.print_quiz(generator)
    logger.info(quiz)

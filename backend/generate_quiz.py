from typing import Generator, Optional
import logging
import json
import os
from response_stream_parser import ResponseStreamParser

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
    # Define the list of supported models.
    SUPPORTED_MODELS = [
        "gpt-3.5-turbo",
        "gpt-4-turbo",
        "o1-mini",
        "o3-mini",
        "gemini/gemini-pro",
        "gemini/gemini-2.0-flash",
        "gemini/gemini-1.5-pro-latest",
        "azure_ai/DeepSeek-R1",
    ]

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

    example_question_2 = json.dumps(
        {
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
        }
    )

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

    @staticmethod
    def check_model_is_supported(model: str) -> str:
        """
        Validate the requested model. If it is not supported, default to "gpt-4-turbo".

        Args:
            model (str): The model name to validate.
            
        Returns:
            str: A supported model name.
        """
        if model not in QuizGenerator.SUPPORTED_MODELS:
            logger.warning(f"Model '{model}' is not supported. Defaulting to 'gpt-4-turbo'.")
            return "gpt-4-turbo"
        return model
        

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-3.5-turbo",
    ):
        """
        Initializes the QuizGenerator.
        If `api_key` is not provided, it is retrieved from the environment.
        Also validates that the requested model is one of the supported models.
        If the model is not supported, defaults to "gpt-4-turbo".

        Args:
            api_key (str, optional): The API key to use. Defaults to None.
            model (str, optional): The model name to use. Defaults to "gpt-3.5-turbo".
        """
        self.check_api_key_from_env()

                # Validate and set the model.
        self.model = QuizGenerator.check_model_is_supported(model)

        # Use the separate parser class to handle the stream.
        self.parser = ResponseStreamParser()

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
        # Use the separate parser class to handle the stream
        parser = ResponseStreamParser()
        return parser.parse_stream(llm_stream)

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

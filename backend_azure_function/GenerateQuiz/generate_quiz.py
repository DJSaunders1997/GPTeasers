# https://github.com/openai/openai-python
from openai import OpenAI
import logging
import json
import os

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class QuizGenerator:
    EXAMPLE_RESPONSE = json.dumps([{
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
    }])

    def __init__(self):
        # Read env var and create openai client object
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "Environment variable OPENAI_API_KEY is not set. "
                "Please ensure it's set and try again."
            )
        self.client = OpenAI(api_key=api_key)

    def generate_quiz(self, topic: str, difficulty: str, n_questions: str = "10") -> str:
        """
        Generate a quiz based on the provided topic and difficulty using OpenAI API.

        Parameters:
        - topic (str): The subject for the quiz, e.g., 'Roman History'.
        - difficulty (str): The desired difficulty of the quiz e.g., 'Easy', 'Medium'.
        - n_questions (str, optional): Number of questions required. Defaults to '10'.

        Returns:
        - str: JSON-formatted quiz questions. If an error occurs, an empty string is returned.
        """
        role = self._create_role(topic, difficulty, n_questions)

        logging.info(f"Role content for OpenAI API: {role}")

        try:
            completion = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": role}]
            )
            response = completion.choices[0].message.content
            logging.debug(f"Raw OpenAI response: {response}")

            cleaned_response = response[response.find("["): response.find("]") + 1]
            logging.debug(f"Cleaned response: {cleaned_response}")

            formatted_response = json.loads(cleaned_response)
            return json.dumps(formatted_response, indent=2)

        except json.JSONDecodeError as je:
            logging.error(f"JSON decoding error: {je}. Response causing error: {response}")
            return ""

        except Exception as e:
            logging.error(f"General error when calling OpenAI API: {e}")
            return ""

    def _create_role(self, topic: str, difficulty: str, n_questions: str) -> str:
        return (
            f"You are an AI to generate quiz questions. "
            f"You will be given a topic e.g. Roman History with a difficulty of Normal. "
            f"Give {n_questions} responses in a json format such as: {self.EXAMPLE_RESPONSE}. "
            f"Your task is to generate similar responses for {topic} "
            f"with the difficulty of {difficulty}. "
            f"ENSURE THESE ARE CORRECT. DO NOT INCLUDE INCORRECT ANSWERS! "
            f"DO NOT PREFIX THE RESPONSE WITH ANYTHING EXCEPT THE RAW JSON!"
        )

if __name__ == "__main__":
    quiz_generator = QuizGenerator()

    topic = "Crested Gecko"
    difficulty = "Medium"
    quiz = quiz_generator.generate_quiz(topic, difficulty, 5)
    print(quiz)

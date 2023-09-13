# https://github.com/openai/openai-python
import openai
import logging
import json
import os

logger = logging.getLogger(__name__)

# Set up OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError(
        "Environment variable OPENAI_API_KEY is not set. Please ensure it's set and try again."
    )
openai.api_key = OPENAI_API_KEY


def generate_quiz(topic: str, n_questions: str = "10") -> str:
    """
    Generate a quiz based on the provided topic using OpenAI API.

    Parameters:
    - topic (str): The subject for the quiz, e.g., 'Roman History'.
    - n_questions (str, optional): Number of questions required. Defaults to '5'.

    Returns:
    - str: JSON-formatted quiz questions.
    """

    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Example response for guiding the AI on the expected format
    example_response = [
        {
            "question_id": 1,
            "question": "Who was the first emperor of Rome?",
            "A": "Julius Caesar",
            "B": "Augustus",
            "C": "Constantine",
            "answer": "B",
            "explanation": "Augustus, originally Octavian, was the first to hold the title of Roman Emperor. Julius Caesar, while pivotal, never held the emperor title.",
            "wikipedia": r"https://en.wikipedia.org/wiki/Augustus",
            "dalle_prompt": "Augustus Caesar looking regal",
        }
    ]

    example_response_string = json.dumps(example_response)

    role = f"""You are an AI to generate quiz questions. 
    You will be given a topic e.g. Roman History. 
    Give {n_questions} responses in a json format such as:
    {example_response_string}.
    Your task is to generate similar responses for {topic}.
    ENSURE THESE ARE CORRECT. DO NOT INCLUDE INCORRECT ANSWERS!
    """

    logging.info(f"{role=}")

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": role}]
        )

        response = completion.choices[0].message.content
        formatted_response = json.loads(response)
        return json.dumps(formatted_response, indent=2)

    except openai.error.OpenAIError as e:
        logger.error(f"Error {e.http_status}: {e.error}")
        return None

    except Exception as e:
        logger.error(f"Non-OpenAI Error when calling OpenAI api: {e}")
        return None


if __name__ == "__main__":
    print("Running main:")

    topic = "Crested Gecko"
    quiz = generate_quiz(topic)
    if quiz:
        print(quiz)
    else:
        print("Failed to generate the quiz.")

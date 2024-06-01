# https://github.com/openai/openai-python
from openai import OpenAI
import logging
import json
import os

logger = logging.getLogger(__name__)

# Set up OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError(
        "Environment variable OPENAI_API_KEY is not set."
        "Please ensure it's set and try again."
    )
client = OpenAI(api_key=OPENAI_API_KEY)


def generate_quiz(topic: str, difficulty: str, n_questions: str = "10") -> str:
    """
    Generate a quiz based on the provided topic and difficulty using OpenAI API.

    Parameters:
    - topic (str): The subject for the quiz, e.g., 'Roman History'.
    - difficulty (str): The desired difficulty of the quiz e.g., 'Easy', 'Medium'.
    - n_questions (str, optional): Number of questions required. Defaults to '10'.

    Returns:
    - str: JSON-formatted quiz questions. If an error occurs, an empty string is returned.
    """

    # Example response for guiding the AI on the expected format
    example_response = [
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
                "Julius Caesar, while pivotal, never held the emperor title. "
            ),
            "wikipedia": r"https://en.wikipedia.org/wiki/Augustus",
        }
    ]

    example_response_string = json.dumps(example_response)

    role = f"""You are an AI to generate quiz questions. 
    You will be given a topic e.g. Roman History with a difficulty of Normal.
    Give {n_questions} responses in a json format such as:
    {example_response_string}.
    Your task is to generate similar responses for {topic} 
    with the difficulty of {difficulty}.
    ENSURE THESE ARE CORRECT. DO NOT INCLUDE INCORRECT ANSWERS!
    DO NOT PREFIX THE RESPONSE WITH ANYTHING EXCEPT THE RAW JSON!
    """

    logging.info(f"{role=}")

    try:
        # Generate text in JSON mode
        # https://platform.openai.com/docs/guides/text-generation/json-mode
        completion = client.chat.completions.create(
            model="gpt-4-turbo-preview", 
            #response_format={ "type": "json_object" },
            messages=[{"role": "user", "content": role}]
        )

        response = completion.choices[0].message.content
        logging.debug(f"Raw OpenAI response: {response}")

        # Remove any prefix or suffix before raw json e.g. ```json\n and remove it
        # I think this is done for code responses so the ChatGPT UI can render code
        cleaned_response = response[response.find("[") : response.find("]") + 1]
        logging.debug(f"Cleaned response: {cleaned_response}")

        formatted_response = json.loads(cleaned_response)
        return json.dumps(formatted_response, indent=2)

    except json.JSONDecodeError as je:
        error_message = f"JSON decoding error: {je}. Response causing error: {response}"
        logging.error(error_message)
        return ""

    except Exception as e:
        error_message = f"General error when calling OpenAI api: {e}"
        logging.error(error_message)
        return ""


if __name__ == "__main__":
    print("Running main:")

    topic = "Crested Gecko"
    difficulty = "Medium"
    quiz = generate_quiz(topic, difficulty)
    if quiz:
        print(quiz)
    else:
        print("Failed to generate the quiz.")

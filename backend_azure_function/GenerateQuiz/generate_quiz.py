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

def generate_quiz(topic: str, difficulty: str, n_questions: str = "10") -> str:
    """
    Generate a quiz based on the provided topic and difficulty using OpenAI API.

    Parameters:
    - topic (str): The subject for the quiz, e.g., 'Roman History'.
    - difficulty (str): The desired difficulty of the quiz e.g., 'Easy', 'Medium'.
    - n_questions (str, optional): Number of questions required. Defaults to '10'.

    Returns:
    - str: JSON-formatted quiz questions.
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
            "explanation": "Augustus, originally Octavian, was the first to hold the title of Roman Emperor. Julius Caesar, while pivotal, never held the emperor title.",
            "wikipedia": r"https://en.wikipedia.org/wiki/Augustus",
        }
    ]

    example_response_string = json.dumps(example_response)

    role = f"""You are an AI to generate quiz questions. 
    You will be given a topic e.g. Roman History with a difficulty of Normal.
    Give {n_questions} responses in a json format such as:
    {example_response_string}.
    Your task is to generate similar responses for {topic} with the difficulty of {difficulty}.
    ENSURE THESE ARE CORRECT. DO NOT INCLUDE INCORRECT ANSWERS!
    """

    logging.info(f"{role=}")

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": role}]
        )

        response = completion.choices[0].message.content
        logging.debug(f"Raw OpenAI response: {response}")

        formatted_response = json.loads(response)
        return json.dumps(formatted_response, indent=2)

    except openai.error.OpenAIError as e:
        error_message = f"OpenAI API Error {e.http_status}: {e.error}"
        logger.error(error_message)
        return json.dumps({"error": error_message})

    except json.JSONDecodeError as je:
        error_message = f"JSON decoding error: {je}. Response causing error: {response}"
        logging.error(error_message)
        return json.dumps({"error": error_message})

    except Exception as e:
        error_message = f"General error when calling OpenAI api: {e}"
        logging.error(error_message)
        return json.dumps({"error": error_message})

if __name__ == "__main__":
    print("Running main:")

    topic = "Crested Gecko"
    difficulty = "Medium"
    quiz = generate_quiz(topic, difficulty)
    if quiz:
        print(quiz)
    else:
        print("Failed to generate the quiz.")

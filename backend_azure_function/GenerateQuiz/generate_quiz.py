from openai import OpenAI
import logging
import json
import os

logger = logging.getLogger(__name__)

# Set up OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("Environment variable OPENAI_API_KEY is not set. Please ensure it's set and try again.")

# Initialize OpenAI client with the API key
client = OpenAI(api_key=OPENAI_API_KEY)

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
            "options": {"A": "Julius Caesar", "B": "Augustus", "C": "Constantine"},
            "answer": "B",
            "explanation": "Augustus, originally Octavian, was the first Roman Emperor. Julius Caesar, while pivotal, never held the emperor title.",
            "wikipedia": r"https://en.wikipedia.org/wiki/Augustus"
        }
    ]

    example_response_string = json.dumps(example_response)

    role = f"""You are an AI designed to generate quiz questions. 
    Generate {n_questions} quiz questions about {topic} at a {difficulty} difficulty level in JSON format similar to: {example_response_string}.
    Ensure the answers are correct."""
    logging.info(f"{role=}")

    try:
        # Generate text in JSON mode
        # https://platform.openai.com/docs/guides/text-generation/json-mode
        completion = client.chat.completions.create(
            model="gpt-4-turbo-preview", 
            response_format={ "type": "json_object" },
            messages=[{"role": "user", "content": role}]
        )

        response = completion.choices[0].message.content
        logging.debug(f"Raw OpenAI response: {response}")
        return json.dumps(response, indent=2)

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

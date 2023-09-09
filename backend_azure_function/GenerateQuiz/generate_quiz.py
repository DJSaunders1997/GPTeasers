# https://github.com/openai/openai-python
import openai
import json
import os

def generate_quiz(topic: str, n_questions: str = "5") -> str:
    """
    Generate a quiz based on the provided topic using OpenAI API.
    
    Parameters:
    - topic (str): The subject for the quiz, e.g., 'Roman History'.
    - n_questions (str, optional): Number of questions required. Defaults to '5'.
    
    Returns:
    - str: JSON-formatted quiz questions.
    """

    # Set up OpenAI API key from environment variables
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

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": role}]
        )

        response = completion.choices[0].message.content
        formatted_response = json.loads(response)
        return json.dumps(formatted_response, indent=2)

    except openai.error.OpenAIError as e:
        # Handle the error appropriately for your application
        print(f"Error {e.http_status}: {e.error}")
        return None

if __name__ == "__main__":
    topic = "Hard Roman History"
    quiz = generate_quiz(topic)
    if quiz:
        print(quiz)
    else:
        print("Failed to generate the quiz.")

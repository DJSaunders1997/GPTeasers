# Example of openai streaming 
# https://platform.openai.com/docs/api-reference/streaming
from openai import OpenAI
import os
import json

# Set up OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError(
        "Environment variable OPENAI_API_KEY is not set."
        "Please ensure it's set and try again."
    )
client = OpenAI(api_key=OPENAI_API_KEY)

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
You will be given a topic e.g. Roman History with a difficulty.
Give 10 responses in a json format such as:
{example_response_string}.
Your task is to generate similar responses for Geckos 
with the difficulty of Hard.
ENSURE THESE ARE CORRECT. DO NOT INCLUDE INCORRECT ANSWERS!
DO NOT PREFIX THE RESPONSE WITH ANYTHING EXCEPT THE RAW JSON!
"""

stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": role}],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
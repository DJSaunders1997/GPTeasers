# Example of openai streaming 
# https://platform.openai.com/docs/api-reference/streaming
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI, Stream
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
example_response = {
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

example_response_string = json.dumps(example_response)

role = f"""You are an AI to generate quiz questions. 
You will be given a topic e.g. Roman History with a difficulty.
Give 5 responses in a json format such as:
{example_response_string}.
Your task is to generate similar responses for Geckos 
with the difficulty of Hard.
ENSURE THESE ARE CORRECT. DO NOT INCLUDE INCORRECT ANSWERS!
DO NOT PREFIX THE RESPONSE WITH ANYTHING EXCEPT THE RAW JSON!
RETURN EACH JSON ITEM AS A NEW ROW!
"""

def stream_generator(stream:Stream):
    """Parses streamed data chunks from OpenAI into complete JSON objects and yields them.

    Accumulates data in a buffer and attempts to parse complete JSON objects. If successful,
    the JSON object is yielded as a string and the buffer is cleared for the next object.
    Ignores empty chunks and continues buffering if the JSON is incomplete.

    Similar-ish SSE Fast API blog: https://medium.com/@nandagopal05/server-sent-events-with-python-fastapi-f1960e0c8e4b
    Helpful SO that says about the SSE format of data: {your-json}: https://stackoverflow.com/a/49486869/11902832
    
    Args:
        stream (Stream): Stream from OpenAI's api

    Yields:
        str: Complete JSON object of a quiz question in string representation.
    
    Raises:
        json.JSONDecodeError: If parsing fails due to malformed JSON data.
    """


    buffer = ""
    for chunk in stream:
        chunk_contents = chunk.choices[0].delta.content
        # Ignore empty chunks. TODO: ensure this doesnt go on forever lol
        if chunk_contents is None:
            print("Chunk was empty!")
            continue
        buffer += chunk_contents  # Append new data to buffer
        try:
            while buffer:
                obj = json.loads(buffer)  # Try to parse buffer as JSON
                print(f"Successfully parsed response as JSON object! {obj}")
                formatted_sse = f"data: {json.dumps(obj)}\n\n"  # Format as SSE
                print(f"Successfully formated data as SSE event: {formatted_sse}")
                yield formatted_sse  # Yield the JSON string
                buffer = ""  # Clear buffer since JSON was successfully parsed
        except json.JSONDecodeError:
            continue  # Continue buffering if JSON is incomplete
    
    print("Finished stream!")

# Test if you just wanna run and see the response generator working
if __name__ == "__main__":
    print("I'm in main!")
    for item in stream_generator(stream):
        print(item, end="")


app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/stream-quiz-questions")
async def stream_quiz_questions():
    """
    Streams AI-generated quiz questions as JSON via a continuous HTTP response. 
    Uses `StreamingResponse` to send data in real-time before the full response is ready, 
    suitable for long-running data streams. Learn more at:
    https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse
    """

    # Create new stream per request
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": role}],
        stream=True,
    )

    # Ensure stream is properly initialized and configured here.
    generator = stream_generator(stream)  # Adjust as needed based on actual stream setup

    return StreamingResponse(generator, media_type="text/event-stream")

# Run with uvicorn streaming_example:app --reload --log-level debug
# Access with curl http://localhost:8000/stream-quiz-questions
# This simple example works!
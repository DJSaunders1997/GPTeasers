# Example of openai streaming 
# https://platform.openai.com/docs/api-reference/streaming
import logging
from generate_quiz import QuizGenerator
from generate_image import generate_image
from fastapi import FastAPI, Request
from fastapi.responses import (StreamingResponse, JSONResponse)
from fastapi.middleware.cors import CORSMiddleware

# Copy Azure Docs Example
# https://github.com/Azure-Samples/fastapi-on-azure-functions/tree/main
app = FastAPI()

# Set up CORS for locally testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/GenerateQuiz")
async def generate_quiz_endpoint(request: Request) -> JSONResponse:
    """ 
    FastAPI App to generate an image based on a provided prompt.

    The function expects a 'prompt' parameter in the HTTP request query
    or body. If a valid prompt is received, the function uses the
    generate_image() function to create an image URL corresponding to
    the prompt and returns it in the HTTP response.

    Parameters:
    - request (Request): The FastAPI request object containing the client request.

    Returns:
    - JSONResponse: The HTTP response object containing the generated quiz or
                    an appropriate error message.
    """

    topic = request.query_params.get("topic")
    difficulty = request.query_params.get("difficulty")
    n_questions = request.query_params.get("n_questions")

    logging.info(f"Python HTTP trigger function processed a request with {topic=} {difficulty=}, {n_questions=}.")

    # If either 'topic' or 'difficulty' is not provided in the request, 
    # the function will return an error message and a 400 status code.
    # n_questions is optional
    if not topic or not difficulty:
        error_message = "Please provide a topic and difficulty in the query string or in the request body to generate a quiz."
        logging.error(error_message)
        return JSONResponse(
            content={"error": error_message},
            status_code=400,
        )

    # Set default value if not set
    if not n_questions:
        n_questions = 10
    
    logging.info(
        f"Generating quiz for topic: {topic} with difficulty: {difficulty} with number of questions: {n_questions}"
    )

    # TODO: rename to quiz creator
    # TODO: Fix - currently doesnt actually stream, but returns all items at once.
    # Need to look into the azure functions streaming capability
    # Or think about hosting the fastapi in another method e.g. ACI
    quiz_generator = QuizGenerator()
    generator = quiz_generator.generate_quiz(topic, difficulty, n_questions)

    return StreamingResponse(generator, media_type="text/event-stream")

@app.get("/GenerateImage")
async def generate_image_endpoint(request: Request) -> JSONResponse:
    """ 
    FastAPI App to generate an image based on a provided prompt.

    The function expects a 'prompt' parameter in the HTTP request query
    or body. If a valid prompt is received, the function uses the
    generate_image() function to create an image URL corresponding to
    the prompt and returns it in the HTTP response.

    Parameters:
    - request (Request): The FastAPI request object containing the client request.

    Returns:
    - JSONResponse: The HTTP response object containing the image URL or
                    an appropriate error message.
    """

    logging.info("Python HTTP trigger function processed a request.")

    prompt = request.query_params.get("prompt")

    if not prompt:
        error_message = "No prompt query param provided for image generation."
        logging.warning(error_message)
        return JSONResponse(content={"error": error_message}, status_code=400)

    logging.info(f"Received prompt: {prompt}")
    image_url = generate_image(prompt)

    if image_url is None:
        error_message = "Error - Image generation failed."
        logging.error(error_message)
        return JSONResponse(content={"error": error_message}, status_code=500)

    # Return the image URL in the HTTP response
    logging.info(f"Generated image for prompt {prompt}: {image_url}")
    return JSONResponse(content={"image_url": image_url}, status_code=200)

# Run with uvicorn fastapi_generate_quiz:app --reload --host 0.0.0.0 --port 8000 --log-level debug
# Access with curl "http://localhost:8000/GenerateQuiz?topic=UK%20History&difficulty=easy&n_questions=3"
# Access with curl "http://localhost:8000/GenerateImage?prompt=A%20Juicy%20Burger"
# This simple example works!
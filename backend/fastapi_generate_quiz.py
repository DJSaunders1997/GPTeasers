# Example of openai streaming
# https://platform.openai.com/docs/api-reference/streaming
import logging
from generate_quiz import QuizGenerator
from generate_image import ImageGenerator
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

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
async def generate_quiz_endpoint(
    topic: str = Query(..., description="The subject for the quiz (e.g., 'UK History')"),
    difficulty: str = Query(..., description="The desired difficulty (e.g., 'easy', 'medium', 'hard')"),
    n_questions: int = Query(10, description="Number of questions to generate (defaults to 10)"),
    model: Optional[str] = Query(None, description="The model to use. If not provided, the default from QuizGenerator is used")
) -> StreamingResponse:
    """
    FastAPI endpoint to generate a quiz based on topic, difficulty, and model.

    Query Parameters:
      - topic: The subject for the quiz (e.g., "UK History").
      - difficulty: The desired difficulty (e.g., "easy", "medium").
      - n_questions: (Optional) Number of questions to generate (defaults to 10).
      - model: (Optional) The model to use. If not provided, the default from QuizGenerator is used.

    Returns:
      - StreamingResponse: Streams quiz questions in SSE format.
    """
    logging.info(
        f"Python HTTP trigger function processed a request with {topic=} {difficulty=}, {n_questions=}, model={model}."
    )

    logging.info(
        f"Generating quiz with: {topic=}, {difficulty=}, {n_questions=}, {model=}."
    )

    # Create a QuizGenerator instance.
    # TODO: rename to quiz creator ?
    if model is not None:
        quiz_generator = QuizGenerator(model=model)
    else:
        quiz_generator = QuizGenerator()
    generator = quiz_generator.generate_quiz(topic, difficulty, n_questions)

    # Return the quiz as a streaming response in SSE format.
    return StreamingResponse(generator, media_type="text/event-stream")


@app.get("/GenerateImage")
async def generate_image_endpoint(
    prompt: str = Query(..., description="The prompt for image generation")
) -> JSONResponse:
    """
    FastAPI endpoint to generate an image based on a provided prompt.

    Query Parameters:
      - prompt: The prompt for image generation.

    Returns:
      - JSONResponse: Contains the generated image URL or an error message.
    """
    logging.info("Processing image generation request.")
    
    logging.info(f"Received image prompt: {prompt}")
    image_generator = ImageGenerator()
    image_url = image_generator.generate_image(prompt)

    if image_url is None:
        error_message = "Error - Image generation failed."
        logging.error(error_message)
        return JSONResponse(content={"error": error_message}, status_code=500)

    logging.info(f"Generated image for prompt '{prompt}': {image_url}")
    return JSONResponse(content={"image_url": image_url}, status_code=200)


# Run with uvicorn fastapi_generate_quiz:app --reload --host 0.0.0.0 --port 8000 --log-level debug
# Access with curl "http://localhost:8000/GenerateQuiz?topic=UK%20History&difficulty=easy&n_questions=3"
# Access with curl "http://localhost:8000/GenerateImage?prompt=A%20Juicy%20Burger"
# This simple example works!

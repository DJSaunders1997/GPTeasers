# GPTeasers FastAPI Backend
# AI-powered quiz generation and image creation service
# https://platform.openai.com/docs/api-reference/streaming
import logging
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse

from generate_image import ImageGenerator
from generate_quiz import QuizGenerator

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Copy Azure Docs Example
# https://github.com/Azure-Samples/fastapi-on-azure-functions/tree/main
app = FastAPI(
    title="GPTeasers AI Quiz Generator",
    description="""
    ## GPTeasers Backend API

    A powerful AI-driven service for generating educational quizzes and images
    using multiple AI providers including OpenAI, Gemini, Azure AI, and DeepSeek.

    ### Features:
    - **Real-time Quiz Streaming**: Generate quiz questions with Server-Sent Events
    - **Multiple AI Providers**: Support for OpenAI, Gemini, Azure AI, DeepSeek models
    - **Dynamic Image Generation**: Create contextual images using DALL-E
    - **Flexible Configuration**: Customizable difficulty levels and question counts
    - **Dynamic Model Discovery**: Frontend automatically syncs with available models

    ### Supported AI Models:
    - OpenAI: gpt-3.5-turbo, gpt-4-turbo, o1-mini, o3-mini
    - Google Gemini: gemini-2.0-flash, gemini-1.5-pro-latest
    - Azure AI: DeepSeek-R1 and other Azure-hosted models

    ### Usage Examples:
    - Quiz Generation: `/GenerateQuiz?topic=Python&difficulty=medium&n_questions=5`
    - Image Creation: `/GenerateImage?prompt=A beautiful sunset over mountains`
    - Model Discovery: `/SupportedModels`

    ### Architecture:
    - Streams quiz questions in real-time using Server-Sent Events (SSE)
    - Uses LiteLLM for universal AI provider abstraction
    - CORS enabled for frontend integration
    - Comprehensive error handling and logging
    """,
    version="1.0.0",
    contact={
        "name": "GPTeasers Development Team",
        "email": "DJSaunders1997@gmail.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://github.com/DJSaunders1997/GPTeasers/blob/main/LICENSE",
    },
)

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
    topic: str = Query(
        ..., description="The subject for the quiz (e.g., 'UK History')"
    ),
    difficulty: str = Query(
        ..., description="The desired difficulty (e.g., 'easy', 'medium', 'hard')"
    ),
    n_questions: int = Query(
        10, description="Number of questions to generate (defaults to 10)"
    ),
    model: Optional[str] = Query(
        None,
        description="The model to use. If not provided, the default from QuizGenerator is used",
    ),
) -> StreamingResponse:
    """
    FastAPI endpoint to generate a quiz based on topic, difficulty, and model.

    Query Parameters:
      - topic: The subject for the quiz (e.g., "UK History").
      - difficulty: The desired difficulty (e.g., "easy", "medium").
      - n_questions: (Optional) Number of questions to generate (defaults to 10).
    - model: (Optional) AI model to use; defaults to QuizGenerator's default.

    Returns:
      - StreamingResponse: Streams quiz questions in SSE format.
    """
    logger.info(
        f"Quiz request: topic={topic}, difficulty={difficulty}, "
        f"n_questions={n_questions}, model={model}"
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


@app.get("/SupportedModels")
async def get_supported_models() -> JSONResponse:
    """
    FastAPI endpoint to retrieve the list of supported AI models.

    Returns:
      - JSONResponse: Contains an array of supported model names.
    """
    logger.info("Retrieving supported models list.")

    supported_models = QuizGenerator.SUPPORTED_MODELS

    logger.info(f"Returning {len(supported_models)} supported models.")
    return JSONResponse(content={"models": supported_models}, status_code=200)


@app.get("/GenerateImage")
async def generate_image_endpoint(
    prompt: str = Query(..., description="The prompt for image generation"),
) -> JSONResponse:
    """
    FastAPI endpoint to generate an image based on a provided prompt.

    Query Parameters:
      - prompt: The prompt for image generation.

    Returns:
      - JSONResponse: Contains the generated image URL or an error message.
    """
    logger.info("Processing image generation request.")

    logger.info(f"Received image prompt: {prompt}")
    image_generator = ImageGenerator()
    image_url = image_generator.generate_image(prompt)

    if image_url is None:
        error_message = "Error - Image generation failed."
        logger.error(error_message)
        return JSONResponse(content={"error": error_message}, status_code=500)

    logger.info(f"Generated image for prompt '{prompt}': {image_url}")
    return JSONResponse(content={"image_url": image_url}, status_code=200)


# Run with uvicorn fastapi_generate_quiz:app --reload --host 0.0.0.0 --port 8000 --log-level debug
# Access with curl "http://localhost:8000/GenerateQuiz?topic=UK%20History&difficulty=easy&n_questions=3"
# Access with curl "http://localhost:8000/GenerateImage?prompt=A%20Juicy%20Burger"
# This simple example works!

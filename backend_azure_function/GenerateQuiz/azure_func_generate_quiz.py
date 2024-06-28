# Example of openai streaming 
# https://platform.openai.com/docs/api-reference/streaming
import logging
from .generate_quiz import QuizGenerator
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import azure.functions as func

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
async def main(request: Request) -> JSONResponse:
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

    logging.info("Python HTTP trigger function processed a request.")

    topic = request.query_params.get("topic")
    difficulty = request.query_params.get("difficulty")


    # If either 'topic' or 'difficulty' is not provided in the request, 
    # the function will return an error message and a 400 status code.
    if not topic or not difficulty:
        error_message = "Please provide a topic and difficulty in the query string or in the request body to generate a quiz."
        logging.error(error_message)
        return JSONResponse(
            content={"error": error_message},
            status_code=400,
        )

    logging.info(
        f"Generating quiz for topic: {topic} with difficulty: {difficulty}"
    )

    # TODO: rename to quiz creator
    # TODO: Fix - currently doesnt actually stream, but returns all items at once.
    # Need to look into the azure functions streaming capability
    # Or think about hosting the fastapi in another method e.g. ACI
    quiz_generator = QuizGenerator()
    generator = quiz_generator.generate_quiz(topic, difficulty)

    return StreamingResponse(generator, media_type="text/event-stream")

# https://dev.to/manukanne/azure-functions-and-fastapi-14b6
def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse: # noqa F811
    return func.AsgiMiddleware(app).handle(req, context)
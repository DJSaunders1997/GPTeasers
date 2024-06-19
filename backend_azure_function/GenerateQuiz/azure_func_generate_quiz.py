import logging
from .generate_quiz import generate_quiz
import fastapi
from fastapi import Request
from fastapi.responses import JSONResponse
import azure.functions as func

# Copy Azure Docs Example
# https://github.com/Azure-Samples/fastapi-on-azure-functions/tree/main
app = fastapi.FastAPI()

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

    quiz = generate_quiz(topic, difficulty)

    if quiz == "":  # Will be empty if theres an error
        error_message = "Error - Quiz generation returned an empty string."
        logging.error(error_message)
        return JSONResponse(content={"error": error_message}, status_code=500)
    
    logging.info(f"Quiz generation successful.\n{quiz}")
    return JSONResponse({"quiz": quiz}, status_code=200)

# https://dev.to/manukanne/azure-functions-and-fastapi-14b6
def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return func.AsgiMiddleware(app).handle(req, context)
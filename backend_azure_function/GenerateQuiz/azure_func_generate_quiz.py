import logging
from azure.functions import HttpRequest, HttpResponse
from .generate_quiz import generate_quiz


def main(req: HttpRequest) -> HttpResponse:
    """Azure Function to generate a quiz based on a provided topic and difficulty.

    The function expects a 'topic' parameter in the HTTP request query
    or body. If a valid topic is received, the function uses the
    generate_quiz() function to create an image URL corresponding to
    the prompt and returns it in the HTTP response.

    Parameters:
    - req (HttpRequest): The HTTP request object containing the client request.

    Returns:
    - HttpResponse: The HTTP response object containing the generated quiz or
                    an appropriate error message.
    """
    logging.info("Python HTTP trigger function processed a request.")

    topic = req.params.get("topic")
    difficulty = req.params.get("difficulty")

    if topic and difficulty:
        logging.info(f"Generating quiz for topic: {topic} with difficulty: {difficulty}")
        try:
            quiz = generate_quiz(topic, difficulty)
            if "error" in quiz:  # Check for the error key in the response.
                logging.error(quiz)
                return HttpResponse(quiz, status_code=500)
            logging.info(f"Quiz generation successful.\n{quiz}")
            return HttpResponse(quiz, status_code=200)

        except Exception as e:
            error_message = f"Error generating quiz: {str(e)}"
            logging.error(error_message)
            return HttpResponse(error_message, status_code=500)
    else:
        logging.error("No topic and/or difficulty provided in request.")
        return HttpResponse(
            "Please provide a topic and difficulty in the query string or in the request body to generate a quiz.",
            status_code=400,
        )
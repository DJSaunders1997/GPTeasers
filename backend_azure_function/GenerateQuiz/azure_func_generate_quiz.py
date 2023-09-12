import logging
from azure.functions import HttpRequest, HttpResponse
from .generate_quiz import generate_quiz


def main(req: HttpRequest) -> HttpResponse:
    """Azure Function to generate an image based on a provided topic.

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
    if not topic:
        logging.debug("Topic not found in request parameters, trying request body...")
        try:
            req_body = req.get_json()
        except ValueError:
            logging.warning("Error decoding JSON from request body.")
            pass
        else:
            topic = req_body.get("topic")

    if topic:
        logging.info(f"Generating quiz for topic: {topic}")
        try:
            # The generate_quiz() function returns the quiz based on the provided topic
            quiz = generate_quiz(topic)

            # Return the generated quiz in the HTTP response
            logging.info(f"Quiz generation successful.\n{quiz}")
            return HttpResponse(quiz, status_code=200)

        except Exception as e:
            logging.error(f"Error generating quiz: {str(e)}")
            # Handle exceptions that might occur during quiz generation
            return HttpResponse(f"Error generating quiz: {str(e)}", status_code=500)
    else:
        logging.warning("No topic provided in request.")
        return HttpResponse(
            "Please provide a topic in the query string or in the request body to generate a quiz.",
            status_code=400,
        )

import logging
from azure.functions import HttpRequest, HttpResponse
from .generate_quiz import generate_quiz


def main(req: HttpRequest) -> HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    topic = req.params.get("topic")
    if not topic:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            topic = req_body.get("topic")

    if topic:
        try:
            # The generate_quiz() function returns the quiz based on the provided topic
            quiz = generate_quiz(topic)

            # Return the generated quiz in the HTTP response
            return HttpResponse(f"Generated Quiz: {quiz}", status_code=200)

        except Exception as e:
            # Handle exceptions that might occur during quiz generation
            return HttpResponse(f"Error generating quiz: {str(e)}", status_code=500)
    else:
        return HttpResponse(
            "Please provide a topic in the query string or in the request body to generate a quiz.",
            status_code=400,
        )

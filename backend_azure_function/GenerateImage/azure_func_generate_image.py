import logging
from azure.functions import HttpRequest, HttpResponse
from .generate_image import generate_image


def main(req: HttpRequest) -> HttpResponse:
    """
    Azure Function to generate an image based on a provided prompt.

    The function expects a 'prompt' parameter in the HTTP request query
    or body. If a valid prompt is received, the function uses the
    generate_image() function to create an image URL corresponding to
    the prompt and returns it in the HTTP response.

    Parameters:
    - req (HttpRequest): The HTTP request object containing the client request.

    Returns:
    - HttpResponse: The HTTP response object containing the image URL or
                    an appropriate error message.
    """
    logging.info("Python HTTP trigger function processed a request.")

    prompt = req.params.get("prompt")

    if not prompt:
        error_message = "No prompt query param provided for image generation."
        logging.warning(error_message)
        return HttpResponse(error_message, status_code=400)

    logging.info(f"Received prompt: {prompt}")
    image_url = generate_image(prompt)

    if image_url is None:
        error_message = "Error - Image generation failed."
        logging.error(error_message)
        return HttpResponse(error_message, status_code=500)

    # Return the image URL in the HTTP response
    logging.info(f"Generated image for prompt {prompt}: {image_url}")
    return HttpResponse(image_url, status_code=200)





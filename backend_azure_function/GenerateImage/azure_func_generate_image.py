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
        try:
            req_body = req.get_json()
        except ValueError as e:
            logging.warning(f"Error decoding JSON: {str(e)}")
            pass
        else:
            prompt = req_body.get("prompt")

    if prompt:
        logging.info(f"Received prompt: {prompt}")
        try:
            # generate_image() function returns the URL of the generated image
            image_url = generate_image(prompt)
            logging.info(f"Generated image for prompt {prompt}: {image_url}")

            # Return the image URL in the HTTP response
            return HttpResponse(image_url, status_code=200)

        except Exception as e:
            logging.error(f"Error generating image for prompt {prompt}: {str(e)}")
            # Handle exceptions that might occur during image generation
            return HttpResponse(f"Error generating image: {str(e)}", status_code=500)
    else:
        logging.warning("No prompt provided for image generation.")
        return HttpResponse(
            "Please provide a prompt in the query string " 
            "or in the request body to generate an image.",
            status_code=400,
        )

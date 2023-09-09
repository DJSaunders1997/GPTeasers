import logging
from azure.functions import HttpRequest, HttpResponse
from .generate_image import generate_image

def main(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    prompt = req.params.get('prompt')
    if not prompt:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            prompt = req_body.get('prompt')

    if prompt:
        try:
            # generate_image() function returns the URL of the generated image
            image_url = generate_image(prompt)

            # Return the image URL in the HTTP response
            return HttpResponse(f"Generated Image URL: {image_url}", status_code=200)

        except Exception as e:
            # Handle exceptions that might occur during image generation
            return HttpResponse(f"Error generating image: {str(e)}", status_code=500)
    else:
        return HttpResponse(
            "Please provide a prompt in the query string or in the request body to generate an image.",
            status_code=400
        )

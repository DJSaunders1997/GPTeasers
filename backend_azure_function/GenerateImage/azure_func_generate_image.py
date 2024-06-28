import logging
from .generate_image import generate_image
import fastapi
from fastapi import Request
from fastapi.responses import JSONResponse
import azure.functions as func

# Copy Azure Docs Example
# https://github.com/Azure-Samples/fastapi-on-azure-functions/tree/main
app = fastapi.FastAPI()
# https://iotespresso.com/azure-function-to-fastapi-app-service/
# Might not need CORS 
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

# @app.get("/api/GenerateImage")
@app.get("/GenerateImage")
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
    - JSONResponse: The HTTP response object containing the image URL or
                    an appropriate error message.
    """

    logging.info("Python HTTP trigger function processed a request.")

    prompt = request.query_params.get("prompt")

    if not prompt:
        error_message = "No prompt query param provided for image generation."
        logging.warning(error_message)
        return JSONResponse(content={"error": error_message}, status_code=400)

    logging.info(f"Received prompt: {prompt}")
    image_url = generate_image(prompt)

    if image_url is None:
        error_message = "Error - Image generation failed."
        logging.error(error_message)
        return JSONResponse(content={"error": error_message}, status_code=500)

    # Return the image URL in the HTTP response
    logging.info(f"Generated image for prompt {prompt}: {image_url}")
    return JSONResponse(content={"image_url": image_url}, status_code=200)

# https://dev.to/manukanne/azure-functions-and-fastapi-14b6
def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse: # noqa F811
    return func.AsgiMiddleware(app).handle(req, context)
# refactored_openai_image.py

from openai import OpenAI

import logging
import os

logger = logging.getLogger(__name__)

# Set up OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError(
        "Environment variable OPENAI_API_KEY is not set. " 
        "Please ensure it's set and try again."
    )

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_image(prompt: str, n: int = 1, size: str = "256x256") -> str:
    """
    Generates an image using OpenAI's Image API based on a given prompt.

    Parameters:
    - prompt (str): The textual description for the image to be generated.
    - n (int): The number of images to generate. Default is 1.
    - size (str): The size of the generated image. Default is "256x256".

    Returns:
    - str: URL of generated image, in JSON dict with key URL

    Raises:
    - openai.error.OpenAIError: If there's an error in the request.
    """


    logging.info(f"{prompt=}")

    try:
        response = client.images.generate(prompt=prompt, n=n, size=size)
        return response.data[0].url
    except Exception as e:
        logger.error(f"Non-OpenAI Error when calling OpenAI api: {e}")
        return None


if __name__ == "__main__":
    image_description = (
        "Crested Gecko showcasing its distinct crests and coloration. Pixel Art"
    )
    image_url = generate_image(image_description)
    if image_url:
        print(f"Generated Image URL: {image_url}")

from openai import OpenAI
import logging
import os

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class ImageGenerator:
    def __init__(self):
        """
        Initializes the ImageGenerator by setting up the OpenAI client with the API key from environment variables.
        Raises an error if the API key is not set.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "Environment variable OPENAI_API_KEY is not set. "
                "Please ensure it's set and try again."
            )
        self.client = OpenAI(api_key=api_key)

    def generate_image(self, prompt: str, n: int = 1, size: str = "256x256") -> str:
        """
        Generates an image using OpenAI's Image API based on a given prompt.

        Parameters:
        - prompt (str): The textual description for the image to be generated.
        - n (int): The number of images to generate. Default is 1.
        - size (str): The size of the generated image. Default is "256x256".

        Returns:
        - str: URL of generated image in JSON dict with key URL, or None in case of an error.
        """
        logging.info(f"Generating image with prompt: {prompt=}")

        try:
            response = self.client.images.generate(prompt=prompt, n=n, size=size)
            return response.data[0].url
        except Exception as e:
            logger.error(f"Error when calling OpenAI API: {e}")
            return None

if __name__ == "__main__":
    image_generator = ImageGenerator()
    image_description = "Crested Gecko showcasing its distinct crests and coloration. Pixel Art"
    image_url = image_generator.generate_image(image_description)
    if image_url:
        print(f"Generated Image URL: {image_url}")

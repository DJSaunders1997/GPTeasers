import os
import logging
from typing import Optional
from openai import OpenAI

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ImageGenerator:
    @classmethod
    def get_api_key_from_env(cls) -> str:
        """Retrieves the OpenAI API key from environment variables.

        Returns:
            str: The API key from the environment variable OPENAI_API_KEY.

        Raises:
            ValueError: If the environment variable is not set or empty.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "Environment variable OPENAI_API_KEY is not set. "
                "Please ensure it's set and try again."
            )
        return api_key

    def __init__(self, api_key: Optional[str] = None):
        """Initialises the ImageGenerator.

        If `api_key` is not provided, it is retrieved from the environment
        using `get_api_key_from_env`.

        Args:
            api_key (str, optional): The OpenAI API key to use. Defaults to None.
        """
        if api_key is None:
            api_key = self.get_api_key_from_env()

        self.client = OpenAI(api_key=api_key)

    def generate_image(self, prompt: str, n: int = 1, size: str = "256x256") -> Optional[str]:
        """Generates an image based on the provided prompt.

        Args:
            prompt (str): The textual description for the image to be generated.
            n (int, optional): The number of images to generate. Defaults to 1.
            size (str, optional): The size of the generated image. Defaults to "256x256".

        Returns:
            Optional[str]: The URL of the generated image if successful,
            or `None` if an error occurred.
        """
        logger.info(f"Generating image with prompt: {prompt=}")
        image_url = self._get_image_url(prompt, n, size)
        logger.info(f"Generated image URL: {image_url}")
        return image_url
    
    def _get_image_url(self, prompt: str, n: int, size: str) -> Optional[str]:
        """Makes the API call to generate images using OpenAI and returns the URL.

        Args:
            prompt (str): The textual description for the image to be generated.
            n (int): The number of images to generate.
            size (str): The size of the generated image (e.g., "256x256").

        Returns:
            Optional[str]: The URL of the first generated image,
            or `None` if an error occurred.
        """
        try:
            response = self.client.images.generate(prompt=prompt, n=n, size=size)
            return response.data[0].url
        except Exception as e:
            logger.error(f"Error when calling OpenAI API: {e}")
            return None


if __name__ == "__main__":
    # Example usage:
    image_generator = ImageGenerator() # Uses environment variable if no API key is provided
    prompt_text = "Crested Gecko showcasing its distinct crests and colouration. Pixel Art"
    image_url = image_generator.generate_image(prompt_text)

# refactored_openai_image.py

import openai
import os

def generate_image(prompt: str, n: int = 1, size: str = "256x256") -> str:
    """
    Generates an image using OpenAI's Image API based on a given prompt.

    Parameters:
    - prompt (str): The textual description for the image to be generated.
    - n (int): The number of images to generate. Default is 1.
    - size (str): The size of the generated image. Default is "256x256".

    Returns:
    - str: URL of the generated image.

    Raises:
    - openai.error.OpenAIError: If there's an error in the request.
    """
    
    # Authenticate with OpenAI API
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    try:
        response = openai.Image.create(prompt=prompt, n=n, size=size)
        return response['data'][0]['url']
    except openai.error.OpenAIError as e:
        print(f"Error Code: {e.http_status}")
        print(f"Error Message: {e.error}")
        return None

if __name__ == "__main__":
    image_description = "Hannibal Barca leading his army through the Alps. Realistic Dramatic"
    image_url = generate_image(image_description)
    if image_url:
        print(f"Generated Image URL: {image_url}")

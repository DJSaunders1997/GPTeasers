import os
import pytest
from backend.generate_image import ImageGenerator

"""
Test file for ImageGenerator class.

Grouped into:
1. **Unit Tests**: Tests class behavior using mocks (no real API calls).
2. **Integration Tests**: Makes real API calls to OpenAI (run manually/staging only).
"""

@pytest.fixture
def image_generator():
    """Fixture to create an instance of ImageGenerator"""
    return ImageGenerator()


class TestImageGeneratorUnit:
    """
    Unit tests for ImageGenerator class.
    Uses mocker to avoid real API calls.
    """
    
    def test_generate_image_success(self, mocker, image_generator):
        """Test generate_image with a successful API response."""
        mock_response = mocker.Mock()
        mock_response.data = [{"url": "https://example.com/generated_image.png"}]

        mocker.patch.object(image_generator.client.images, "generate", return_value=mock_response)

        url = image_generator.generate_image("A test prompt")
        assert url == "https://example.com/generated_image.png"

    def test_generate_image_custom_size(self, mocker, image_generator):
        """Test generate_image with a custom image size."""
        mock_response = mocker.Mock()
        mock_response.data = [{"url": "https://example.com/custom_size_image.png"}]

        mocker.patch.object(image_generator.client.images, "generate", return_value=mock_response)

        url = image_generator.generate_image("A dragon flying over mountains", size="512x512")
        assert url == "https://example.com/custom_size_image.png"

    def test_generate_image_api_failure(self, mocker, image_generator):
        """Test generate_image when OpenAI API raises an exception."""
        mocker.patch.object(image_generator.client.images, "generate", side_effect=Exception("API request failed"))

        url = image_generator.generate_image("A cyberpunk city at night")
        assert url is None

    def test_generate_image_invalid_prompt(self, image_generator):
        """Test generate_image with an invalid (empty) prompt."""
        assert image_generator.generate_image("") is None

    def test_openai_api_key_not_set(self, mocker):
        """Test that an error is raised if the OpenAI API key is not set in the environment variables."""
        mocker.patch.dict(os.environ, {}, clear=True)  # Simulate missing API key
        
        with pytest.raises(ValueError, match="Environment variable OPENAI_API_KEY is not set"):
            ImageGenerator()
    
    def test_logging_when_api_fails(self, mocker, image_generator):
        """Test that errors are properly logged when the OpenAI API fails."""
        mock_logger = mocker.patch("backend.generate_image.logger.error")
        mocker.patch.object(image_generator.client.images, "generate", side_effect=Exception("API failure"))

        image_generator.generate_image("Test prompt")
        mock_logger.assert_called_with("Error when calling OpenAI API: API failure")


class TestImageGeneratorIntegration:
    """
    Integration tests for ImageGenerator class.
    These tests make real API calls and should be run manually.
    """
    
    @pytest.mark.integration
    def test_generate_image_real_api(self):
        """Calls the real OpenAI API and verifies it returns a valid URL."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            pytest.skip("Skipping test: OPENAI_API_KEY is not set.")

        image_generator = ImageGenerator()
        prompt = "A futuristic city skyline at sunset"

        url = image_generator.generate_image(prompt)

        assert url is not None, "Expected a valid URL, but got None."
        assert url.startswith("http"), f"Unexpected URL format: {url}"

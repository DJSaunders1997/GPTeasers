import pytest
import os
from backend.generate_image import generate_image

"""
Test file for generate_image function.

Grouped into:
1. **Unit Tests**: Tests function behavior using mocks (no real API calls).
2. **Integration Tests**: Makes real API calls to OpenAI (run manually/staging only).
"""

class TestGenerateImageUnit:
    """
    Unit tests for generate_image function.
    Uses mocker to avoid real API calls.
    """
    
    def test_generate_image_success(self, mocker):
        """Test generate_image with a successful API response."""
        mocker.patch("backend.generate_image.client.images.generate", 
                     return_value=mocker.Mock(data=[mocker.Mock(url="https://example.com/generated_image.png")]))
        
        url = generate_image("A test prompt")
        assert url == "https://example.com/generated_image.png"

    def test_generate_image_custom_size(self, mocker):
        """Test generate_image with a custom image size."""
        mocker.patch("backend.generate_image.client.images.generate", 
                     return_value=mocker.Mock(data=[mocker.Mock(url="https://example.com/custom_size_image.png")]))
        
        url = generate_image("A dragon flying over mountains", size="512x512")
        assert url == "https://example.com/custom_size_image.png"

    def test_generate_image_api_failure(self, mocker):
        """Test generate_image when OpenAI API raises an exception."""
        mocker.patch("backend.generate_image.client.images.generate", side_effect=Exception("API request failed"))
        
        url = generate_image("A cyberpunk city at night")
        assert url is None

    def test_generate_image_invalid_prompt(self):
        """Test generate_image with an invalid (empty) prompt."""
        assert generate_image("") is None

    def test_openai_api_key_not_set(self):
        """Test that an error is raised if the OpenAI API key is not set in the environment variables."""
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]
        
        with pytest.raises(ValueError, match="Environment variable OPENAI_API_KEY is not set"):
            generate_image("A test prompt")
    
    def test_logging_when_api_fails(self, mocker):
        """Test that errors are properly logged when the OpenAI API fails."""
        mock_logger = mocker.patch("backend.generate_image.logger.error")
        mocker.patch("backend.generate_image.client.images.generate", side_effect=Exception("API failure"))
        
        generate_image("Test prompt")
        mock_logger.assert_called_with("Non-OpenAI Error when calling OpenAI api: API failure")


class TestGenerateImageIntegration:
    """
    Integration tests for generate_image function.
    These tests make real API calls and should be run manually.
    """
    
    @pytest.mark.integration
    def test_generate_image_real_api(self):
        """Calls the real OpenAI API and verifies it returns a valid URL."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            pytest.skip("Skipping test: OPENAI_API_KEY is not set.")

        prompt = "A futuristic city skyline at sunset"
        
        url = generate_image(prompt)
        
        assert url is not None, "Expected a valid URL, but got None."
        assert url.startswith("http"), f"Unexpected URL format: {url}"

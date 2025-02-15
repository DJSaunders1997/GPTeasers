import os
import pytest
import logging
from unittest.mock import patch, MagicMock
from backend.generate_quiz import QuizGenerator

"""
Test file for QuizGenerator class.

Grouped into:
1. **Unit Tests**: Tests class behavior using mocks (no real API calls).
2. **Integration Tests**: Makes real API calls to OpenAI (run manually/staging only).

This file demonstrates how to use fixtures, monkeypatching, and method patching to isolate
code under test and simulate various conditions.
"""


@pytest.fixture
def quiz_generator(monkeypatch):
    """Fixture to create an instance of QuizGenerator with dummy API keys.
    So that the class can initialize without error."""
    monkeypatch.setenv("OPENAI_API_KEY", "dummy_key")
    monkeypatch.setenv("GEMINI_API_KEY", "dummy_key")
    monkeypatch.setenv("DEEPSEEK_API_KEY", "dummy_key")
    monkeypatch.setenv("AZURE_AI_API_KEY", "dummy_key")
    monkeypatch.setenv("AZURE_AI_API_BASE", "https://dummy.azure.com")

    return QuizGenerator()


class TestQuizGenerator:
    """Unit tests for the QuizGenerator class."""

    def test_check_model_is_supported(self):
        """Test that unsupported models default to 'gpt-4-turbo'."""
        assert (
            QuizGenerator.check_model_is_supported("unsupported-model") == "gpt-4-turbo"
        )
        assert (
            QuizGenerator.check_model_is_supported("gpt-3.5-turbo") == "gpt-3.5-turbo"
        )

    def test_environment_variable_not_set(self, monkeypatch):
        """
        Test that initializing QuizGenerator without an API key (i.e. if the environment variable
        is not set) raises a ValueError.

        We remove the environment variable and expect the constructor to raise an error.
        """
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        with pytest.raises(
            ValueError, match="Environment variable OPENAI_API_KEY is not set"
        ):
            QuizGenerator()

    def test_create_role(self, quiz_generator):
        """
        Test that the _create_role method produces a prompt that contains the expected parameters.

        The role prompt should include the topic, difficulty, number of questions, and the example JSON.
        """
        topic = "Science"
        difficulty = "Easy"
        n_questions = 5
        role = quiz_generator._create_role(topic, difficulty, n_questions)
        # Check that the output string includes our input values and the example JSON
        assert topic in role
        assert difficulty in role
        assert str(n_questions) in role
        assert quiz_generator.EXAMPLE_RESPONSE in role

    @patch("backend.generate_quiz.completion")
    def test_generate_quiz(self, mock_completion, quiz_generator):
        """Test generate_quiz to ensure it streams responses properly."""
        mock_stream = iter(['{"question": "What is 2+2?", "answer": "4"}\n'])
        mock_completion.return_value = mock_stream

        parser_mock = MagicMock()
        parser_mock.parse_stream.return_value = iter(
            ['data: {"question": "What is 2+2?", "answer": "4"}\n\n']
        )

        with patch.object(quiz_generator, "parser", parser_mock):
            generator = quiz_generator.generate_quiz("Math", "Easy", n_questions=1)
            result = list(generator)

        assert result == ['data: {"question": "What is 2+2?", "answer": "4"}\n\n']

    def test_print_quiz(self, quiz_generator, caplog):
        """Test that print_quiz correctly logs the generated questions."""
        caplog.set_level(logging.INFO)
        test_generator = iter(['data: {"question": "What is 2+2?", "answer": "4"}\n\n'])
        result = quiz_generator.print_quiz(test_generator)
        assert 'data: {"question": "What is 2+2?", "answer": "4"}\n\n' in result


class TestQuizGeneratorIntegration:
    """
    Integration tests for the QuizGenerator class.
    These tests make real API calls and are skipped by default, unless explicitly requested.
    """

    @pytest.mark.integration
    def test_generate_quiz_real_api(self):
        """
        Integration test that calls the real OpenAI API.

        This test will only run if the OPENAI_API_KEY is set in the environment. It verifies that the
        generate_quiz method returns at least one SSE-formatted result.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            pytest.skip("Skipping integration test: OPENAI_API_KEY not set.")
        quiz_gen = QuizGenerator()
        topic = "Math"
        difficulty = "Hard"
        gen = quiz_gen.generate_quiz(topic, difficulty, 2)
        # Collect the output from the generator.
        results = list(gen)
        # Verify that at least one SSE event is produced.
        assert len(results) > 0
        for r in results:
            assert r.startswith("data: ")

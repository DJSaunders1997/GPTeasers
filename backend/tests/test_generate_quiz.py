import os
import json
import pytest
from types import SimpleNamespace
from backend.generate_quiz import QuizGenerator

"""
Test file for QuizGenerator class.

Grouped into:
1. **Unit Tests**: Tests class behavior using mocks (no real API calls).
2. **Integration Tests**: Makes real API calls to OpenAI (run manually/staging only).

This file demonstrates how to use fixtures, monkeypatching, and method patching to isolate
code under test and simulate various conditions.
"""

# Fixture to create an instance of QuizGenerator with a dummy API key.
@pytest.fixture
def quiz_generator(monkeypatch):
    # Set a dummy API key in the environment so that the class can initialize without error.
    monkeypatch.setenv("OPENAI_API_KEY", "dummy_key")
    return QuizGenerator()


class TestQuizGeneratorUnit:
    """
    Unit tests for the QuizGenerator class.
    These tests use mocks to avoid making real API calls.
    """

    def test_get_api_key_from_env(self, monkeypatch):
        """
        Test that get_api_key_from_env correctly retrieves the API key from the environment.

        We set the environment variable and then call the class method to verify that it returns
        the expected API key.
        """
        monkeypatch.setenv("OPENAI_API_KEY", "test_key")
        key = QuizGenerator.get_api_key_from_env()
        assert key == "test_key"

    def test_environment_variable_not_set(self, monkeypatch):
        """
        Test that initializing QuizGenerator without an API key (i.e. if the environment variable
        is not set) raises a ValueError.

        We remove the environment variable and expect the constructor to raise an error.
        """
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        with pytest.raises(ValueError, match="Environment variable OPENAI_API_KEY is not set"):
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

    def test_create_openai_stream(self, mocker, quiz_generator):
        """
        Test that _create_openai_stream calls the underlying OpenAI API with the correct parameters.

        We use method patching (with mocker.patch.object) to replace the actual API call with a dummy
        value, then verify that the method was called with the correct parameters.
        """
        dummy_role = "dummy role string"
        dummy_stream = "dummy stream"
        # Patch the client's chat.completions.create method so no actual API call is made.
        patcher = mocker.patch.object(
            quiz_generator.client.chat.completions, "create", return_value=dummy_stream
        )
        result = quiz_generator._create_openai_stream(dummy_role)
        # Verify the patched method was called once with the expected arguments.
        patcher.assert_called_once_with(
            model="gpt-4-turbo-preview",
            messages=[{"role": "user", "content": dummy_role}],
            stream=True
        )
        assert result == dummy_stream

    def test_create_question_generator(self, quiz_generator):
        """
        Test the _create_question_generator method by simulating a stream that yields a single chunk
        containing a complete JSON string.

        We use a fake chunk (wrapped in a SimpleNamespace) to simulate what the OpenAI API might return.
        """
        # Use the EXAMPLE_RESPONSE as our fake complete JSON content.
        fake_json = quiz_generator.EXAMPLE_RESPONSE
        fake_chunk = SimpleNamespace(
            choices=[SimpleNamespace(delta=SimpleNamespace(content=fake_json))]
        )

        def fake_stream():
            # Yield a single fake chunk.
            yield fake_chunk

        # Call the generator method and check that it yields the correctly formatted SSE event.
        gen = quiz_generator._create_question_generator(fake_stream())
        expected = "data: " + json.dumps(json.loads(fake_json)) + "\n\n"
        result = next(gen)
        assert result == expected

    def test_empty_chunk_in_question_generator(self, quiz_generator, mocker):
        """
        Test _create_question_generator when the stream yields an empty chunk (i.e., a chunk with None content)
        before yielding a valid JSON chunk.

        This verifies that the method correctly logs the empty chunk and then proceeds once valid data is received.
        """
        fake_json = quiz_generator.EXAMPLE_RESPONSE
        # Create a chunk that simulates an empty response.
        empty_chunk = SimpleNamespace(
            choices=[SimpleNamespace(delta=SimpleNamespace(content=None))]
        )
        # Then a chunk that contains valid JSON.
        valid_chunk = SimpleNamespace(
            choices=[SimpleNamespace(delta=SimpleNamespace(content=fake_json))]
        )

        def fake_stream():
            yield empty_chunk
            yield valid_chunk

        # Patch logger.debug to capture log messages about empty chunks.
        logger_debug = mocker.patch("backend.generate_quiz.logger.debug")
        gen = quiz_generator._create_question_generator(fake_stream())
        result = next(gen)
        # Verify that the empty chunk log was produced.
        logger_debug.assert_any_call("Chunk was empty!")
        expected = "data: " + json.dumps(json.loads(fake_json)) + "\n\n"
        assert result == expected

    def test_format_sse(self):
        """
        Test that _format_sse correctly formats a JSON object as an SSE (Server-Sent Event) string.

        This is a simple helper method that should return a string starting with "data:".
        """
        sample_dict = {"key": "value"}
        expected = "data: " + json.dumps(sample_dict) + "\n\n"
        result = QuizGenerator._format_sse(sample_dict)
        assert result == expected

    def test_validate_and_parse_json_valid(self):
        """
        Test validate_and_parse_json with a valid JSON string.

        The method should return the corresponding Python dictionary.
        """
        valid_json_str = '{"foo": "bar"}'
        result = QuizGenerator.validate_and_parse_json(valid_json_str)
        assert result == {"foo": "bar"}

    def test_validate_and_parse_json_incomplete(self):
        """
        Test validate_and_parse_json with an incomplete JSON string.

        Since the method is designed to return None if the JSON is incomplete (not fully formed),
        we expect the result to be None.
        """
        incomplete_json_str = '{"foo": "bar"'
        result = QuizGenerator.validate_and_parse_json(incomplete_json_str)
        assert result is None

    def test_print_quiz(self, mocker, quiz_generator):
        """
        Test the static print_quiz method by passing in a dummy generator.

        We patch logger.info to verify that the print_quiz method logs each quiz item correctly.
        """
        dummy_generator = (s for s in ["data: {\"quiz\": \"q1\"}\n\n", "data: {\"quiz\": \"q2\"}\n\n"])
        logger_info = mocker.patch("backend.generate_quiz.logger.info")
        QuizGenerator.print_quiz(dummy_generator)
        # Verify that logger.info was called with the expected messages.
        logger_info.assert_any_call("Item 1: data: {\"quiz\": \"q1\"}\n\n")
        logger_info.assert_any_call("Item 2: data: {\"quiz\": \"q2\"}\n\n")


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

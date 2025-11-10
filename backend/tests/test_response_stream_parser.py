from types import SimpleNamespace

import pytest

from backend.response_stream_parser import ResponseStreamParser

"""
Test file for ResponseStreamParser class.

Grouped into:
1. **Unit Tests**: Tests class behavior using mocks (no real API calls).
2. **Integration Tests**: Processes real stream responses.

This file uses fixtures, monkeypatching, and method patching to isolate
code under test and simulate various conditions.
"""


@pytest.fixture
def response_parser():
    return ResponseStreamParser()


class TestResponseStreamParser:
    """
    Unit tests for the ResponseStreamParser class.
    """

    def test_extract_chunk_content_valid(self, response_parser):
        """
        Test extracting content from a valid chunk.
        """
        chunk = SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content="test content"))])
        content = response_parser._extract_chunk_content(chunk)
        assert content == "test content"

    def test_extract_chunk_content_invalid(self, response_parser):
        """
        Test that an invalid chunk returns None.
        """
        chunk = SimpleNamespace(choices=[])
        content = response_parser._extract_chunk_content(chunk)
        assert content is None

    def test_split_buffer(self, response_parser):
        """
        Test splitting the buffer into complete lines and a remainder.
        """
        response_parser.buffer = '{"question": "Who was ..."}\n{"question": "What is ..."}\nincomplete'

        expected_complete_lines = [
            '{"question": "Who was ..."}',
            '{"question": "What is ..."}',
        ]
        expected_remainder = "incomplete"

        complete_lines, remainder = response_parser._split_buffer()

        print("Complete Lines:", complete_lines)
        print("Remainder:", remainder)

        assert complete_lines == expected_complete_lines, (
            f"Expected complete lines '{expected_complete_lines}', but got {complete_lines}"
        )

        assert remainder == expected_remainder, f"Expected remainder '{expected_remainder}', but got {remainder}"

    def test_process_line_valid_json(self, response_parser):
        """
        Test processing a valid JSON line.
        """
        line = '{"question": "Who was the first emperor of Rome?"}'
        result = response_parser._process_line(line)
        assert result == 'data: {"question": "Who was the first emperor of Rome?"}\n\n'

    def test_process_line_invalid_json(self, response_parser):
        """
        Test processing an invalid JSON line.
        """
        line = '{"question": "Who was the first emperor of Rome?"'
        result = response_parser._process_line(line)
        assert result is None

    def test_parse_stream(self, response_parser):
        """
        Test parsing a simulated LLM stream.
        """
        fake_stream = iter(
            [
                SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content='{"question": "First"}\n'))]),
                SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content='{"question": "Second"}\n'))]),
            ]
        )
        results = list(response_parser.parse_stream(fake_stream))
        assert results == [
            'data: {"question": "First"}\n\n',
            'data: {"question": "Second"}\n\n',
        ]

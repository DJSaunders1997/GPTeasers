import json
import logging
from typing import Generator, Optional

logger = logging.getLogger(__name__)


class ResponseStreamParser:
    """
    A class responsible for processing streaming responses from an LLM and parse into JSON objects.

    Parses streamed data chunks from the LLM into complete JSON objects and yields them as SSE strings.

    Accumulates data in a buffer and attempts to parse complete JSON objects. If successful,
    the JSON object is yielded as a string and the buffer is cleared for the next object.
    Ignores empty chunks and continues buffering if the JSON is incomplete.

    Similar-ish SSE Fast API blog: https://medium.com/@nandagopal05/server-sent-events-with-python-fastapi-f1960e0c8e4b
    Helpful SO that says about the SSE format of data: {your-json}: https://stackoverflow.com/a/49486869/11902832

    Methods:
      - parse_stream(llm_stream): Processes an LLM stream and yields complete SSE-formatted JSON objects.
      - _extract_chunk_content(chunk): Extracts text content from a single chunk.
      - _split_buffer(): Splits the internal buffer on newline characters into complete lines and a remainder.
      - _process_line(line): Parses a single line as JSON and formats it as an SSE string.

    Example:
        Suppose the LLM returns chunks that, when combined, look like:

            '{"question_id": 1, "question": "Who was the first emperor of Rome?", ...}\n'
            '{"question_id": 2, "question": "Which Roman Emperor issued the Edict on Maximum Prices?", ...}\n'

        The parser will:
          - Accumulate these chunks into a buffer.
          - Split the buffer on newlines.
          - Parse each complete JSON line.
          - Format each parsed JSON as:

                data: {"question_id": 1, ...}\n\n

          - Yield each formatted SSE string.
    """

    def __init__(self):
        self.buffer = ""

    # Public Method
    def parse_stream(self, llm_stream) -> Generator[str, None, None]:
        """
        Processes the LLM stream and yields complete SSE-formatted JSON objects.

        For each chunk in the stream:
          - The private method _extract_chunk_content is used to get text content.
          - This content is appended to the internal buffer.
          - When the buffer contains one or more newline characters, the private method _split_buffer
            splits it into complete lines and a remainder.
          - Each complete line is processed by _process_line to parse it as JSON and format it as an SSE string.
          - The formatted string is then yielded.

        After the stream ends, any remaining data in the buffer is processed similarly.

        Args:
            llm_stream: An iterable or generator yielding chunks from the LLM.

        Yields:
            SSE-formatted strings, each representing a complete JSON object.
        """
        for chunk in llm_stream:
            # Extract text from the chunk.
            content = self._extract_chunk_content(chunk)
            if content is None:
                logger.debug("Received an empty or invalid chunk; skipping...")
                continue

            # Append the new content to the buffer.
            self.buffer += content

            # If the buffer contains a newline, process the complete lines.
            if "\n" in self.buffer:
                complete_lines, self.buffer = self._split_buffer()
                for line in complete_lines:
                    sse_line = self._process_line(line)
                    if sse_line is not None:
                        yield sse_line

        # After processing all chunks, process any remaining data in the buffer.
        if self.buffer.strip():
            logging.warning(f"Unprocessed data in the buffer! {self.buffer=}")
            sse_line = self._process_line(self.buffer)
            if sse_line is not None:
                yield sse_line

        logger.info("Finished processing the stream!")

    def _extract_chunk_content(self, chunk) -> Optional[str]:
        """
        Extracts text content from a given chunk.

        Expected chunk structure (example):
            {
                "choices": [
                    {
                        "delta": {
                            "content": "some text..."
                        }
                    }
                ]
            }

        If the chunk does not follow the expected structure, a debug message is logged,
        and None is returned.

        Args:
            chunk: A single chunk from the LLM stream.

        Returns:
            The extracted text (str) if available; otherwise, None.
        """
        try:
            return chunk.choices[0].delta.content
        except (AttributeError, IndexError, KeyError):
            logger.debug("Chunk format unexpected or chunk is empty!")
            return None

    def _split_buffer(self) -> (list[str], str):
        """
        Splits the internal buffer on newline characters.

        Since each complete JSON object is expected to end with a newline,
        this function splits the buffer into complete lines and a remaining
        (possibly incomplete) portion.

        Example:
            If self.buffer is:
                '{"question": "Who was ..."}\n"question": "What is ..."}\nincomplete'
            Then:
                complete_lines = ['{"question": "Who was ..."}', '{"question": "What is ..."}']
                remainder = "incomplete"

        Returns:
            A tuple (list of complete JSON lines, remainder string).
        """
        if "\n" not in self.buffer:
            return [], self.buffer  # No full lines, everything is remainder

        lines = self.buffer.split("\n")

        # The remainder is empty if the buffer ends with a newline.
        if self.buffer.endswith("\n"):
            return lines[:-1], ""

        # Otherwise, the last line is incomplete.
        return lines[:-1], lines[-1]

    def _process_line(self, line: str) -> Optional[str]:
        """
        Processes a single line by parsing it as JSON and formatting it as an SSE string.

        Steps:
          1. Strip any leading or trailing whitespace.
          2. If the line is empty, return None.
          3. Attempt to parse the line as JSON.
          4. If parsing is successful, format the JSON object as an SSE string:

                 data: <json-string>\n\n

          5. If parsing fails, log a debug message and return None.

        Example:
            Input: '{"question_id": 1, "question": "Who was the first emperor of Rome?"}'
            Output: 'data: {"question_id": 1, "question": "Who was the first emperor of Rome?"}\n\n'

        Args:
            line: The line of text to process.

        Returns:
            An SSE-formatted string if parsing is successful; otherwise, None.
        """
        line = line.strip()
        if not line:
            return None
        try:
            json_obj = json.loads(line)
            return f"data: {json.dumps(json_obj)}\n\n"
        except json.JSONDecodeError as e:
            logger.debug(f"Error parsing line '{line}': {e}")
            return None

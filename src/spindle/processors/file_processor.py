from spindle.abstracts import AbstractFileProcessor
from typing import List
import logging

__All__ = ["FileProcessor"]


class FileProcessor(AbstractFileProcessor):
    """Concrete implementation of AbstractFileProcessor."""

    def process(self, file_path: str) -> List[str]:
        """Processes a single file and returns its content as a list of strings.

        Args:
            file_path (str): The path to the file to be processed.

        Returns:
            List[str]: The processed content of the file.
        """
        content = []
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as code_file:
                for line in code_file:
                    line = line.rstrip()
                    if line and not line.startswith("#"):
                        line = self.remove_non_ascii(line)
                        content.append(line)
        except IOError as e:
            logging.error(f"Failed to process file {file_path}: {e}")
        return content

    @staticmethod
    def remove_non_ascii(text: str) -> str:
        """Removes non-ASCII characters from a string using encoding."""
        return text.encode("ascii", errors="ignore").decode("ascii")

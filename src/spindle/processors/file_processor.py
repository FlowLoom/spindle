from spindle.abstracts import AbstractProcessor
from typing import List
import logging

__All__ = ['FileProcessor']

# TODO: Deprecated; remove in future release
class FileProcessor(AbstractProcessor):
    def process(self, content: str) -> List[str]:
        """
        Process the content of a file.

        Args:
            content (str): The content of the file as a string.

        Returns:
            List[str]: A list of processed lines from the file.
        """
        processed_lines = []
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith("#"):
                line = self.remove_non_ascii(line)
                processed_lines.append(line)
        return processed_lines

    @staticmethod
    def remove_non_ascii(text: str) -> str:
        """
        Remove non-ASCII characters from a string.

        Args:
            text (str): The input string.

        Returns:
            str: The input string with all non-ASCII characters removed.
        """
        return text.encode("ascii", errors="ignore").decode("ascii")
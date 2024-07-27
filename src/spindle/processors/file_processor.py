from spindle.abstracts import AbstractFileProcessor
from typing import List
import logging

__All__ = ["FileProcessor"]


class FileProcessor(AbstractFileProcessor):
    """
    Concrete implementation of AbstractFileProcessor for processing files.

    This class provides methods to read and process file contents, removing empty lines,
    comments, and non-ASCII characters.
    """

    def process(self, file_path: str) -> List[str]:
        """
        Process a single file and return its content as a list of strings.

        This method reads the file, removes empty lines, comments, and non-ASCII characters.
        It handles IOErrors and logs them using the logging module.

        Args:
            file_path (str): The path to the file to be processed.

        Returns:
            List[str]: The processed content of the file as a list of strings.

        Raises:
            IOError: If there's an issue reading the file (caught and logged internally).
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
        """
        Remove non-ASCII characters from a string using encoding.

        This method encodes the input string to ASCII, ignoring non-ASCII characters,
        then decodes it back to a string, effectively removing all non-ASCII characters.

        Args:
            text (str): The input string containing potential non-ASCII characters.

        Returns:
            str: The input string with all non-ASCII characters removed.
        """
        return text.encode("ascii", errors="ignore").decode("ascii")

from typing import List
import re
from spindle.abstracts import AbstractProcessor

__All__ = ['CodeProcessor']


class CodeProcessor(AbstractProcessor):
    """
    A processor for code content that inherits from AbstractProcessor.

    This class provides functionality to process code by removing comments,
    empty lines, and trimming whitespace based on initialization parameters.

    Attributes:
        remove_comments (bool): Flag to determine if comments should be removed.
        remove_empty_lines (bool): Flag to determine if empty lines should be removed.
        trim_lines (bool): Flag to determine if lines should be trimmed.
    """

    def __init__(self, remove_comments: bool = True, remove_empty_lines: bool = True, trim_lines: bool = True):
        """
        Initialize the CodeProcessor with processing options.

        Args:
            remove_comments (bool, optional): Whether to remove comments. Defaults to True.
            remove_empty_lines (bool, optional): Whether to remove empty lines. Defaults to True.
            trim_lines (bool, optional): Whether to trim whitespace from lines. Defaults to True.
        """

        self.remove_comments = remove_comments
        self.remove_empty_lines = remove_empty_lines
        self.trim_lines = trim_lines

    def process(self, content: str) -> List[str]:
        """
        Process the given code content.

        This method overrides the superclass method to handle code processing.

        Args:
            content (str): The code content to be processed.

        Returns:
            List[str]: The processed code as a list of lines.
        """

        return super().process(content)

    def _preprocess(self, content: str) -> List[str]:
        """
        Preprocess the code content by splitting it into lines.

        Args:
            content (str): The code content to be preprocessed.

        Returns:
            List[str]: The code split into lines.
        """

        return content.splitlines()

    def _main_process(self, lines: List[str]) -> List[str]:
        """
        Main processing step for the code.

        This method applies the processing options (trimming, comment removal,
        empty line removal) to each line of code.

        Args:
            lines (List[str]): The lines of code to be processed.

        Returns:
            List[str]: The processed lines of code.
        """

        processed_lines = []
        for line in lines:
            if self.trim_lines:
                line = line.strip()

            if self.remove_comments:
                line = self._remove_comments(line)

            if not self.remove_empty_lines or line:
                processed_lines.append(line)

        return processed_lines

    def _postprocess(self, lines: List[str]) -> List[str]:
        """
        Postprocess the code lines.

        This method is a placeholder for potential post-processing steps.
        Currently, it returns the input lines without modification.

        Args:
            lines (List[str]): The processed lines of code.

        Returns:
            List[str]: The postprocessed lines of code.
        """

        return lines

    def _remove_comments(self, line: str) -> str:
        """
        Remove comments from a line of code.

        This method removes both inline comments and full-line comments.

        Args:
            line (str): A line of code.

        Returns:
            str: The line with comments removed.
        """

        # Remove inline comments
        line = re.sub(r'#.*$', '', line)

        # Remove full-line comments
        if line.lstrip().startswith('#'):
            return ''

        return line

    @staticmethod
    def remove_non_ascii(text: str) -> str:
        """
        Remove non-ASCII characters from a string.

        This method encodes the input string to ASCII, ignoring non-ASCII characters,
        then decodes it back to a string, effectively removing all non-ASCII characters.

        Args:
            text (str): The input string.

        Returns:
            str: The input string with all non-ASCII characters removed.
        """

        return text.encode("ascii", errors="ignore").decode("ascii")

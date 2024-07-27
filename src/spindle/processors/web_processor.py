from spindle.interfaces import IProcessor
from typing import List

__All__ = ['WebProcessor']


class WebProcessor(IProcessor):
    """
    A processor for web content that implements the IProcessor interface.

    This class provides functionality to process web content by splitting it into lines
    and removing empty lines.
    """
    def process(self, content: str) -> List[str]:
        """
        Process the given web content by splitting it into lines and removing empty lines.

        Args:
            content (str): The web content to be processed.

        Returns:
            List[str]: A list of non-empty lines from the processed content.
        """

        # Split the content into lines and remove empty lines
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        return lines

from spindle.interfaces import IProcessor
from typing import List, Any
import logging

__All__ = ["DummyProcessor"]


class DummyProcessor(IProcessor):
    """
    A dummy processor that echoes the input.

    This class implements the IProcessor interface and provides a simple
    echo functionality for demonstration or testing purposes.
    """

    def process(self, echo: Any) -> Any:
        """
        Process the input by returning it unchanged.

        Args:
            echo (Any): The input to be echoed.

        Returns:
            Any: The input value, unchanged.
        """

        content = echo

        return content


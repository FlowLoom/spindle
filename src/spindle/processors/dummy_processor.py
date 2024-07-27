from ct.interfaces import IProcessor
from typing import List, Any
import logging

__All__ = ["DummyProcessor"]


class DummyProcessor(IProcessor):
    """Dummy processor that echoes the input."""

    def process(self, echo: Any) -> Any:

        content = echo

        return content


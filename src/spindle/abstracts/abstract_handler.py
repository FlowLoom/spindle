from spindle.interfaces import IHandler
from abc import abstractmethod
from typing import Dict, List

__All__ = ["AbstractHandler"]


class AbstractHandler(IHandler):
    def handle(self, parsed_files: Dict[str, List[str]]) -> None:
        """Handles the parsed files' content."""
        pass
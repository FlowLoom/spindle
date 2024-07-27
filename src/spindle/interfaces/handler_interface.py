from abc import ABC, abstractmethod
from typing import Dict, List

__All__ = ["IHandler"]


class IHandler(ABC):
    """Interface for handlers."""
    @abstractmethod
    def handle(self, parsed_files: Dict[str, List[str]]) -> None:
        """Handles the parsed files' content."""
        pass

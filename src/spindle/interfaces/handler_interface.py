from abc import ABC, abstractmethod
from typing import Dict, List, Any

__All__ = ["IHandler"]


class IHandler(ABC):
    """
    Interface for handlers.

    This abstract base class defines the interface for handlers that process parsed files.
    """

    @abstractmethod
    def handle(self, parsed_files: Dict[str, List[str]]) -> None:
        """
        Handles the parsed files' content.

        Args:
            parsed_files (Dict[str, List[str]]): A dictionary containing parsed file contents.
                The keys are file names, and the values are lists of strings representing the file content.

        Returns:
            None

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def write(self, data: str) -> None:
        """Write the data to the output destination."""
        pass

    @abstractmethod
    def preprocess(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Preprocess the data before serialization."""
        pass
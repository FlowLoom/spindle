from ct.interfaces import IProcessor
from typing import List

__All__ = ["AbstractFileProcessor"]


class AbstractFileProcessor(IProcessor):
    """Abstract class for file processors."""

    @abstractmethod
    def process(self, file_path: str) -> List[str]:
        """Processes a single file and returns its content as a list of strings.

        Args:
            file_path (str): The path to the file to be processed.

        Returns:
            List[str]: The processed content of the file.
        """
        pass

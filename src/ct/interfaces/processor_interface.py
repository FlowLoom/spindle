from abc import ABC, abstractmethod
from typing import Any

__All__ = ["IProcessor"]


class IProcessor(ABC):
    """Interface for processors."""

    @abstractmethod
    def process(self, item: Any) -> Any:
        """Processes an item and returns the result."""
        pass

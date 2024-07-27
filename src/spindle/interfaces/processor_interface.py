from abc import ABC, abstractmethod
from typing import Any

__All__ = ["IProcessor"]


class IProcessor(ABC):
    """
    Interface for processors.

    This abstract base class defines the interface for processor objects.
    Concrete implementations must override the process method.
    """

    @abstractmethod
    def process(self, item: Any) -> Any:
        """
        Processes an item and returns the result.

        Args:
            item (Any): The item to be processed.

        Returns:
            Any: The processed result.

        Raises:
            NotImplementedError: If the method is not implemented by a concrete subclass.
        """
        pass

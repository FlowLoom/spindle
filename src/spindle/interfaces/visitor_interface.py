from abc import ABC, abstractmethod
from typing import Any

__All__ = ['IVisitor']


class IVisitor(ABC):
    """
    Abstract base class representing a visitor in the Visitor design pattern.

    This class defines the interface for concrete visitor classes.
    """

    @abstractmethod
    def visit(self, element: Any):
        """
        Abstract method to be implemented by concrete visitor classes.

        Args:
            element (Any): The element to be visited.

        Returns:
            None

        Raises:
            NotImplementedError: If the method is not implemented by a concrete subclass.
        """
        pass

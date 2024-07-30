from abc import ABC, abstractmethod
from typing import Any, Dict, List
from .visitable_interface import IVisitable
from .visitor_interface import IVisitor

__All__ = ["IFetcher"]


class IFetcher(IVisitable):
    """
    Abstract base class defining the interface for Fetcher implementations.

    This class inherits from IVisitable, allowing parser instances to be part of a visitor pattern.
    It defines the abstract methods that concrete parser classes must implement.
    """

    @abstractmethod
    def fetch(self, *args: Any, **kwargs: Any) -> Any:
        """
        Fetch content from the given source.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Dict[str, Any]: A dictionary containing the fetched content.
        """
        pass

    @abstractmethod
    def _fetch_content(self, *args: Any, **kwargs: Any) -> Any:
        """
        Fetch raw content from the source.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Any: The raw content fetched from the source
        """
        pass

    @abstractmethod
    def _process_content(self, *args: Any, **kwargs: Any) -> Any:
        """
        Process the content using the associated processor.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Any: The processed content
        """
        pass

    @abstractmethod
    def _format_output(self, *args: Any, **kwargs: Any) -> Any:
        """
        Format the processed content into the expected output structure.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Dict[str, Any]: The formatted output
        """
        pass

    @abstractmethod
    def accept(self, visitor: IVisitor) -> None:
        """
        Accept a visitor to perform operations on this parser.

        Args:
            visitor (IVisitor): The visitor to accept
        """
        pass

    # Note: The accept method is inherited from IVisitable

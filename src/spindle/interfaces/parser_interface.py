from abc import ABC, abstractmethod
from typing import Any, Dict, List
from .visitable_interface import IVisitable
from .visitor_interface import IVisitor

__All__ = ["IParser"]


class IParser(IVisitable):
    """
    Abstract base class defining the interface for parser implementations.

    This class inherits from IVisitable, allowing parser instances to be part of a visitor pattern.
    It defines the abstract methods that concrete parser classes must implement.
    """

    @abstractmethod
    def _fetch_content(self, source: Any) -> Any:
        """
        Fetch raw content from the source.

        Args:
            source (Any): The source from which to fetch content

        Returns:
            Any: The raw content fetched from the source
        """
        pass

    @abstractmethod
    def _process_content(self, content: Any) -> Any:
        """
        Process the content using the associated processor.

        Args:
            content (Any): The content to be processed

        Returns:
            Any: The processed content
        """
        pass

    @abstractmethod
    def _format_output(self, processed_content: Any) -> Dict[str, Any]:
        """
        Format the processed content into the expected output structure.

        Args:
            processed_content (Any): The processed content to format

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
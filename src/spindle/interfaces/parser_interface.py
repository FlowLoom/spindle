from abc import ABC, abstractmethod
from typing import Any, Dict, List
from .visitable_interface import IVisitable

__All__ = ["IParser"]


class IParser(IVisitable):
    """
    An abstract base class for parsing content from various sources.

    This class defines the interface for parsers that can handle different types of sources
    and extract structured content from them. It inherits from IVisitable, allowing for
    visitor pattern implementation.

    Methods:
        parse: Main method to parse content from a given source.
        _fetch_content: Retrieves raw content from the source.
        _extract_content: Extracts relevant information from raw content.
        _process_content: Processes extracted content into a list of strings.
    """

    @abstractmethod
    def parse(self, source: Any) -> Dict[str, List[str]]:
        """
        Parse the content from the given source.

        This method orchestrates the parsing process by calling the other abstract methods
        in the appropriate order.

        Args:
            source (Any): The source to be parsed (e.g., file path, URL, repo path)

        Returns:
            Dict[str, List[str]]: A dictionary containing the parsed content
        """
        pass

    @abstractmethod
    def _fetch_content(self, source: Any) -> Any:
        """
        Fetch raw content from the source.

        This method is responsible for retrieving the raw content from the specified source,
        which could be a file, URL, or repository.

        Args:
            source (Any): The source from which to fetch content

        Returns:
            Any: The raw content fetched from the source
        """

        pass

    @abstractmethod
    def _extract_content(self, raw_content: Any) -> Any:
        """
        Extract relevant content from raw content.

        This method processes the raw content to extract the relevant information needed
        for further processing.

        Args:
            raw_content (Any): The raw content to extract from

        Returns:
            Any: The extracted content
        """

        pass

    @abstractmethod
    def _process_content(self, content: Any) -> List[str]:
        """
        Process the extracted content.

        This method performs the final processing step, converting the extracted content
        into a list of strings.

        Args:
            content (Any): The content to be processed

        Returns:
            List[str]: The processed content as a list of strings
        """

        pass

    # Note: The accept method is inherited from IVisitable
from abc import ABC, abstractmethod
from typing import Dict, List, Any
from spindle.interfaces import IParser, IProcessor

class AbstractParser(IParser):
    """
    An abstract base class for implementing parsers.

    This class provides a skeleton for creating parsers that conform to the IParser interface.
    It includes abstract methods for parsing, fetching, and extracting content, as well as
    a concrete method for processing content using an IProcessor.

    Attributes:
        processor (IProcessor): An instance of a class implementing the IProcessor interface.
    """

    def __init__(self, processor: IProcessor):
        """
        Initialize the AbstractParser with a processor.

        Args:
            processor (IProcessor): An instance of a class implementing the IProcessor interface.
        """

        self.processor = processor

    @abstractmethod
    def parse(self, source: Any) -> Dict[str, List[str]]:
        """
        Parse the given source and return the processed content.

        This method should be implemented by subclasses to define the parsing logic.

        Args:
            source (Any): The source to be parsed.

        Returns:
            Dict[str, List[str]]: A dictionary containing the parsed and processed content.
        """

        pass

    @abstractmethod
    def _fetch_content(self, source: Any) -> Any:
        """
        Fetch raw content from the source.

        This method should be implemented by subclasses to define how to retrieve content from the source.

        Args:
            source (Any): The source from which to fetch content.

        Returns:
            Any: The raw content fetched from the source.
        """

        pass

    @abstractmethod
    def _extract_content(self, raw_content: Any) -> Any:
        """
        Extract relevant content from raw content.

        This method should be implemented by subclasses to define how to extract relevant information from raw content.

        Args:
            raw_content (Any): The raw content to extract from.

        Returns:
            Any: The extracted relevant content.
        """

        pass

    def _process_content(self, content: Any) -> List[str]:
        """
        Process the extracted content using the processor.

        This method uses the IProcessor instance to process the extracted content.

        Args:
            content (Any): The content to be processed.

        Returns:
            List[str]: A list of processed content items.
        """

        return self.processor.process(content)
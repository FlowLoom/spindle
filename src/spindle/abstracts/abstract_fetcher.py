from spindle.interfaces import IFetcher, IProcessor, IVisitor
from abc import abstractmethod
from typing import Any, Dict

__All__ = ['AbstractFetcher']


class AbstractFetcher(IFetcher):
    """
    An abstract base class for parsers that implements the IFetcher interface.

    This class provides a template for creating parsers with a common structure
    for fetching, extracting, processing, and formatting content from various sources.

    Attributes:
        processor (IProcessor): The processor used to process the extracted content.
    """

    def __init__(self, processor: IProcessor):
        """
        Initialize the AbstractParser with a processor.

        Args:
            processor (IProcessor): The processor to be used for content processing.
        """

        self.processor = processor

    def fetch(self, source: Any) -> Dict[str, Any]:
        """
        Parse the content from the given source.

        Args:
            source (Any): The source to be parsed (e.g., file path, URL, repo path)

        Returns:
            Dict[str, Any]: A dictionary containing the parsed content
        """
        raw_content = self._fetch_content(source)
        processed_content = self._process_content(raw_content)
        return self._format_output(processed_content)

    @abstractmethod
    def _fetch_content(self, source: Any) -> Any:
        """
        Fetch raw content from the source.

        This method should be implemented by subclasses to handle specific source types.

        Args:
            source (Any): The source from which to fetch content

        Returns:
            Any: The raw content fetched from the source
        """
        pass

    def _process_content(self, content: Any) -> Any:
        """
        Process the content using the associated processor.

        Args:
            content (Any): The content to be processed

        Returns:
            Any: The processed content
        """
        return self.processor.process(content)

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


    def accept(self, visitor: IVisitor) -> None:
        """
        Accept a visitor to perform operations on this parser.

        Args:
            visitor (IVisitor): The visitor to accept
        """
        visitor.visit(self)
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

    def fetch(self, source: Any, **kwargs: Any) -> Dict[str, Any]:
        """
        Fetch and process the content from the given source.

        Args:
            source: The source to fetch content from.
            **kwargs: Additional keyword arguments.

        Returns:
            Dict[str, Any]: A dictionary containing the fetched and processed content
        """
        raw_content = self._fetch_content(source, **kwargs)
        processed_content = self._process_content(raw_content, **kwargs)
        return self._format_output(processed_content, **kwargs)

    @abstractmethod
    def _fetch_content(self, source: Any, **kwargs: Any) -> Any:
        """
        Fetch raw content from the source.

        Args:
            source: The source to fetch content from.
            **kwargs: Additional keyword arguments.

        Returns:
            Any: The raw content fetched from the source
        """
        pass

    def _process_content(self, content: Any, **kwargs: Any) -> Any:
        """
        Process the content using the associated processor.

        Args:
            content: The content to be processed
            **kwargs: Additional keyword arguments to pass to the processor

        Returns:
            Any: The processed content
        """
        return self.processor.process(content, **kwargs)

    @abstractmethod
    def _format_output(self, processed_content: Any, **kwargs: Any) -> Dict[str, Any]:
        """
        Format the processed content into the expected output structure.

        Args:
            processed_content: The processed content to format
            **kwargs: Additional keyword arguments for formatting

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

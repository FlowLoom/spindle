from typing import Any, Dict, List
from spindle.interfaces import IParser, IVisitor, IProcessor

__All__ = ["AbstractParser"]


class AbstractParser(IParser):
    """
    An abstract base class for parsers that implements the IParser interface.

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

    def parse(self, source: Any) -> Dict[str, List[str]]:
        """
        Parse the content from the given source.

        This method orchestrates the parsing process by calling the fetch, extract,
        and process methods in sequence.

        Args:
            source (Any): The source to be parsed (e.g., file path, URL, repo path)

        Returns:
            Dict[str, List[str]]: A dictionary containing the parsed content
        """

        raw_content = self._fetch_content(source)
        extracted_content = self._extract_content(raw_content)
        processed_content = self._process_content(extracted_content)
        return self._format_output(processed_content)

    def _fetch_content(self, source: Any) -> Any:
        """
        Fetch raw content from the source.

        This method should be implemented by subclasses to handle specific source types.

        Args:
            source (Any): The source from which to fetch content

        Returns:
            Any: The raw content fetched from the source

    def _extract_content(self, raw_content: Any) -> Any:
        """
        Extract relevant content from raw content.

        This method should be implemented by subclasses to handle specific content types.

        Args:
            raw_content (Any): The raw content to extract from

        Returns:
            Any: The extracted content

        Raises:
            NotImplementedError: If not implemented by a subclass
        """
        raise NotImplementedError("_extract_content must be implemented by subclasses")

    def _process_content(self, content: Any) -> Any:
        """
        Process the extracted content using the associated processor.

        Args:
            content (Any): The content to be processed

        Returns:
            Any: The processed content
        """
        return self.processor.process(content)

    def _format_output(self, processed_content: Any) -> Dict[str, List[str]]:
        """
        Format the processed content into the expected output structure.

        This method should be implemented by subclasses if the processed content
        needs to be restructured before returning.

        Args:
            processed_content (Any): The processed content to format

        Returns:
            Dict[str, List[str]]: The formatted output

        Raises:
            NotImplementedError: If not implemented by a subclass
        """
        raise NotImplementedError("_format_output must be implemented by subclasses")

    def accept(self, visitor: IVisitor) -> None:
        """
        Accept a visitor to perform operations on this parser.

        This method implements the Visitor pattern, allowing for operations
        to be performed on the parser without modifying its structure.

        Args:
            visitor (IVisitor): The visitor to accept

        Returns:
            None
        """
        visitor.visit(self)
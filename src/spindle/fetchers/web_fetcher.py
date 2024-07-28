import requests
from typing import Any, Dict, List
from spindle.abstracts import AbstractFetcher
from spindle.interfaces import IProcessor

__All__ = ['WebFetcher']


class WebFetcher(AbstractFetcher):
    """
    A fetcher for web content that inherits from AbstractFetcher.

    This class provides functionality to fetch, process, and format web content.
    """

    def __init__(self, processor: IProcessor):
        """
        Initialize the WebParser with a processor.

        Args:
            processor (IProcessor): An instance of a class implementing the IProcessor interface.
        """

        super().__init__(processor)

    def fetch(self, source: str) -> Dict[str, List[str]]:
        """
        Fetch web content from a given source URL.

        Args:
            source (str): The URL of the web content to parse.

        Returns:
            Dict[str, List[str]]: A dictionary containing the parsed and processed web content.
        """

        raw_content = self._fetch_content(source)
        processed_content = self._process_content(raw_content)
        return self._format_output(processed_content)

    def _fetch_content(self, url: str) -> str:
        """
        Fetch raw content from a given URL.

        Args:
            url (str): The URL to fetch content from.

        Returns:
            str: The raw content of the web page.

        Raises:
            requests.HTTPError: If the HTTP request fails.
        """

        response = requests.get(url)
        response.raise_for_status()
        return response.text

    def _process_content(self, content: str) -> Any:
        """
        Process the raw content using the associated processor.

        Args:
            content (str): The raw content to process.

        Returns:
            Any: The processed content, type depends on the processor implementation.
        """

        return self.processor.process(content)

    def _format_output(self, processed_content: Any) -> Dict[str, List[str]]:
        """
        Format the processed content into a standardized output structure.

        Args:
            processed_content (Any): The content after processing.

        Returns:
            Dict[str, List[str]]: A dictionary with 'web_content' key and processed content as value.
        """

        if isinstance(processed_content, dict) and 'content' in processed_content:
            return {"web_content": processed_content['content']}
        return {"web_content": processed_content}

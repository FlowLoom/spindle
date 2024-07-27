import requests
from bs4 import BeautifulSoup
import re
from spindle.abstracts import AbstractWebParser
from spindle.interfaces import IProcessor
from typing import Dict, List

__All__ = ['WebParser']


class WebParser(AbstractWebParser):
    """
    A web parser that extracts and processes content from web pages using various methods.

    This class provides functionality to fetch web content, extract text using different
    libraries and techniques, and process the extracted text.

    Attributes:
        method (str): The extraction method to use.
        available_methods (List[str]): List of available extraction methods.

    Args:
        processor (IProcessor): An object implementing the IProcessor interface for text processing.
        url (str): The URL of the web page to parse.
        method (str, optional): The extraction method to use. Defaults to 'custom'.

    Raises:
        ImportError: If the specified extraction method is not available.
    """

    def __init__(self, processor: IProcessor, url: str, method: str = 'custom'):
        super().__init__(processor, url)
        self.method = method
        self._check_dependencies()

    def _check_dependencies(self):
        """
        Check and populate the list of available extraction methods based on installed libraries.

        This method attempts to import various content extraction libraries and adds their
        corresponding methods to the available_methods list if successful.

        Raises:
            ImportError: If the specified extraction method is not available.
        """

        self.available_methods = ['custom', 'raw']

        # Check for trafilatura library
        try:
            # Best method for extracting content from web pages
            import trafilatura
            self.available_methods.append('traf')
        except ImportError:
            pass

        # Check for readability library
        try:
            from readability import Document
            self.available_methods.append('readability')
        except ImportError:
            pass

        # Check for article_parser library
        try:
            from article_parser import ArticleParser
            self.available_methods.append('article_parser')
        except ImportError:
            pass

        # Check for boilerpy3 library
        try:
            # TODO: gives a "urllib.error.HTTPError: HTTP Error 403: Forbidden" error
            from boilerpy3 import extractors
            self.available_methods.append('boilerpy3')
        except ImportError:
            pass

        # Check for html2text library
        try:
            import html2text
            self.available_methods.append('html2text')
        except ImportError:
            pass

        # Check for newspaper library
        try:
            import newspaper
            self.available_methods.append('newspaper')
        except ImportError:
            pass

        # Check for goose3 library
        try:
            from goose3 import Goose
            self.available_methods.append('goose')
        except ImportError:
            pass

        if self.method not in self.available_methods:
            raise ImportError(f"The {self.method} method is not available. Please install the required library.")

    def fetch_content(self, url: str) -> str:
        """
        Fetch the raw content from the given URL.

        Args:
            url (str): The URL to fetch content from.

        Returns:
            str: The raw content of the web page.

        Raises:
            requests.exceptions.RequestException: If there's an error fetching the content.
        """

        response = requests.get(url)
        response.raise_for_status()
        return response.text

    def extract_text(self, raw_content: str) -> str:
        """
        Extract text from the raw content using the specified method.

        Args:
            raw_content (str): The raw HTML content to extract text from.

        Returns:
            str: The extracted text.

        Raises:
            ValueError: If an unknown extraction method is specified.
        """

        if self.method == 'custom':
            return self._extract_custom(raw_content)
        elif self.method == 'raw':
            return self.extract_raw(raw_content)
        elif self.method == 'traf':
            return self._extract_with_trafilatura(raw_content)
        elif self.method == 'readability':
            return self._extract_with_readability(raw_content)
        elif self.method == 'article_parser':
            return self._extract_with_article_parser()
        elif self.method == 'boilerpy3':
            return self._extract_with_boilerpy3()
        elif self.method == 'html2text':
            return self._extract_with_html2text(raw_content)
        elif self.method == 'newspaper':
            return self._extract_with_newspaper()
        elif self.method == 'goose':
            return self._extract_with_goose()
        else:
            raise ValueError(f"Unknown extraction method: {self.method}")

    def extract_raw(self, raw_content: str) -> str:
        """
        Extract raw text from HTML content using BeautifulSoup.

        Args:
            raw_content (str): The raw HTML content.

        Returns:
            str: The extracted text.
        """

        soup = BeautifulSoup(raw_content, 'html.parser')
        return soup.get_text()

    def _extract_custom(self, raw_content: str) -> str:
        """
        Custom method to extract text from HTML content.

        This method attempts to identify the main content area and removes scripts,
        styles, and common non-content elements.

        Args:
            raw_content (str): The raw HTML content.

        Returns:
            str: The extracted and cleaned text.
        """

        soup = BeautifulSoup(raw_content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Try to find the main content area
        article = soup.find('article') or soup.find('div', class_=re.compile('article|content|post'))

        if article:
            text = article.get_text()
        else:
            # If no main content area is found, remove common non-content elements
            for elem in soup(['header', 'nav', 'footer', 'aside']):
                elem.decompose()
            text = soup.body.get_text()

        # Clean up the extracted text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return text

    def _extract_with_trafilatura(self, raw_content: str) -> str:
        """
        Extract text using the trafilatura library.

        Args:
            raw_content (str): The raw HTML content.

        Returns:
            str: The extracted text, or an empty string if extraction fails.
        """

        import trafilatura
        return trafilatura.extract(raw_content) or ''

    def _extract_with_readability(self, raw_content: str) -> str:
        """
        Extract text using the readability library.

        Args:
            raw_content (str): The raw HTML content.

        Returns:
            str: The extracted text.
        """

        from readability import Document
        doc = Document(raw_content)
        return doc.summary()

    def _extract_with_article_parser(self) -> str:
        """
        Extract text using the article_parser library.

        Returns:
            str: The extracted content.
        """

        from article_parser import ArticleParser
        parser = ArticleParser()
        article = parser.parse(self.url)
        return article.content

    def _extract_with_boilerpy3(self) -> str:
        """
        Extract text using the boilerpy3 library.

        Returns:
            str: The extracted content.
        """

        from boilerpy3 import extractors
        extractor = extractors.ArticleExtractor()
        return extractor.get_content_from_url(self.url)

    def _extract_with_html2text(self, raw_content: str) -> str:
        """
        Extract text using the html2text library.

        Args:
            raw_content (str): The raw HTML content.

        Returns:
            str: The extracted text.
        """

        import html2text
        h = html2text.HTML2Text()
        h.ignore_links = True
        return h.handle(raw_content)

    def _extract_with_newspaper(self) -> str:
        """
        Extract text using the newspaper library.

        Returns:
            str: The extracted text.
        """

        import newspaper
        article = newspaper.article(self.url)
        article.download()
        article.parse()
        return article.text

    def _extract_with_goose(self) -> str:
        """
        Extract text using the goose3 library.

        Returns:
            str: The extracted text.
        """

        from goose3 import Goose
        g = Goose()
        article = g.extract(url=self.url)
        return article.cleaned_text

    def parse(self) -> Dict[str, List[str]]:
        """
        Parse the content from the given URL.

        This method fetches the content, extracts the text using the specified method,
        and processes the extracted text using the provided processor.

        Returns:
            Dict[str, List[str]]: A dictionary containing the processed web content.
        """

        raw_content = self.fetch_content(self.url)
        text = self.extract_text(raw_content)
        processed_text = self.processor.process(text)
        return {"web_content": processed_text}

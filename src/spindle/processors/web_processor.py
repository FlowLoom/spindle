# In spindle/processors/web_processor.py

from spindle.abstracts import AbstractProcessor
from typing import List, Dict, Any
import re
from bs4 import BeautifulSoup

class WebProcessor(AbstractProcessor):
    """
    A processor for extracting and processing web content from HTML.

    This class provides various methods for content extraction, cleaning, and formatting
    of web pages. It supports multiple extraction methods and configurable processing options.

    Attributes:
        extraction_method (str): The method used for content extraction.
        remove_html (bool): Whether to remove HTML tags from the content.
        remove_excess_whitespace (bool): Whether to remove excess whitespace.
        remove_urls (bool): Whether to remove URLs from the content.
        min_line_length (int): The minimum length of lines to keep.
        max_line_length (int): The maximum length of lines before truncation.
        extract_metadata (bool): Whether to extract metadata from the content.
        available_methods (List[str]): List of available content extraction methods.
    """

    def __init__(self,
                 extraction_method: str = 'custom',
                 remove_html: bool = True,
                 remove_excess_whitespace: bool = True,
                 remove_urls: bool = False,
                 min_line_length: int = 0,
                 max_line_length: int = None,
                 extract_metadata: bool = False):
        """
        Initialize the WebProcessor with the specified configuration.

        Args:
            extraction_method (str): The method to use for content extraction.
            remove_html (bool): Whether to remove HTML tags from the content.
            remove_excess_whitespace (bool): Whether to remove excess whitespace.
            remove_urls (bool): Whether to remove URLs from the content.
            min_line_length (int): The minimum length of lines to keep.
            max_line_length (int): The maximum length of lines before truncation.
            extract_metadata (bool): Whether to extract metadata from the content.
        """

        self.extraction_method = extraction_method
        self.remove_html = remove_html
        self.remove_excess_whitespace = remove_excess_whitespace
        self.remove_urls = remove_urls
        self.min_line_length = min_line_length
        self.max_line_length = max_line_length
        self.extract_metadata = extract_metadata
        self.available_methods = self._check_dependencies()

    def process(self, content: str) -> Dict[str, Any]:
        """
        Process the input content using the configured settings.

        This method overrides the superclass method to handle web content processing.

        Args:
            content (str): The raw HTML content to process.

        Returns:
            Dict[str, Any]: A dictionary containing the processed content and optional metadata.
        """

        return super().process(content)

    def _preprocess(self, content: str) -> str:
        """
        Preprocess the raw HTML content by extracting the main content.

        Args:
            content (str): The raw HTML content.

        Returns:
            str: The extracted main content.
        """

        return self._extract_content(content)

    def _main_process(self, content: str) -> List[str]:
        """
        Process the extracted content according to the configured settings.

        This method applies filters such as whitespace removal, URL removal,
        and line length constraints.

        Args:
            content (str): The extracted content to process.

        Returns:
            List[str]: A list of processed content lines.
        """

        lines = content.split('\n')
        processed_lines = []

        for line in lines:
            line = line.strip()

            if self.remove_excess_whitespace:
                line = re.sub(r'\s+', ' ', line)

            if self.remove_urls:
                line = self._remove_urls(line)

            if len(line) >= self.min_line_length:
                if self.max_line_length and len(line) > self.max_line_length:
                    line = line[:self.max_line_length] + '...'
                processed_lines.append(line)

        return processed_lines

    def _postprocess(self, content: List[str]) -> Dict[str, Any]:
        """
        Postprocess the content and prepare the final output.

        This method combines the processed content lines and optionally extracts metadata.

        Args:
            content (List[str]): The list of processed content lines.

        Returns:
            Dict[str, Any]: A dictionary containing the final content and optional metadata.
        """

        result = {"content": content}

        if self.extract_metadata:
            metadata = self._extract_metadata('\n'.join(content))
            result["metadata"] = metadata

        return result

    def _extract_content(self, raw_content: str) -> str:
        """
        Extract text from the raw HTML content using the specified method.

        Args:
            raw_content (str): The raw HTML content to extract text from.

        Returns:
            str: The extracted text.

        Raises:
            ValueError: If an unknown extraction method is specified.
        """
        if self.extraction_method == 'custom':
            return self._extract_custom(raw_content)
        elif self.extraction_method == 'raw':
            return self._extract_raw(raw_content)
        elif self.extraction_method == 'traf':
            return self._extract_with_trafilatura(raw_content)
        elif self.extraction_method == 'readability':
            return self._extract_with_readability(raw_content)
        elif self.extraction_method == 'article_parser':
            return self._extract_with_article_parser(raw_content)
        elif self.extraction_method == 'boilerpy3':
            return self._extract_with_boilerpy3(raw_content)
        elif self.extraction_method == 'html2text':
            return self._extract_with_html2text(raw_content)
        elif self.extraction_method == 'newspaper':
            return self._extract_with_newspaper(raw_content)
        elif self.extraction_method == 'goose':
            return self._extract_with_goose(raw_content)
        else:
            raise ValueError(f"Unknown extraction method: {self.extraction_method}")

    def _check_dependencies(self) -> List[str]:
        """
        Check and return a list of available extraction methods based on installed libraries.

        Returns:
            List[str]: A list of available extraction methods.
        """
        available_methods = ['custom', 'raw']
        try:
            import trafilatura
            available_methods.append('traf')
        except ImportError:
            pass
        try:
            from readability import Document
            available_methods.append('readability')
        except ImportError:
            pass
        try:
            from article_parser import ArticleParser
            available_methods.append('article_parser')
        except ImportError:
            pass
        try:
            from boilerpy3 import extractors
            available_methods.append('boilerpy3')
        except ImportError:
            pass
        try:
            import html2text
            available_methods.append('html2text')
        except ImportError:
            pass
        try:
            import newspaper
            available_methods.append('newspaper')
        except ImportError:
            pass
        try:
            from goose3 import Goose
            available_methods.append('goose')
        except ImportError:
            pass
        return available_methods

    def _extract_custom(self, raw_content: str) -> str:
        """
        Custom method to extract text from HTML content.

        This method uses BeautifulSoup to parse the HTML and extract relevant content,
        focusing on the article or main content area if available.

        Args:
            raw_content (str): The raw HTML content.

        Returns:
            str: The extracted and cleaned text.
        """

        soup = BeautifulSoup(raw_content, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()
        article = soup.find('article') or soup.find('div', class_=re.compile('article|content|post'))
        if article:
            text = article.get_text()
        else:
            for elem in soup(['header', 'nav', 'footer', 'aside']):
                elem.decompose()
            text = soup.body.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        return '\n'.join(chunk for chunk in chunks if chunk)

    def _extract_raw(self, raw_content: str) -> str:
        """
        Extract raw text from HTML content using BeautifulSoup.

        Args:
            raw_content (str): The raw HTML content.

        Returns:
            str: The extracted text.
        """
        soup = BeautifulSoup(raw_content, 'html.parser')
        return soup.get_text()

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

    def _extract_with_article_parser(self, raw_content: str) -> str:
        """
        Extract text using the article_parser library.

        Args:
            raw_content (str): The raw HTML content.

        Returns:
            str: The extracted content.
        """
        from article_parser import ArticleParser
        parser = ArticleParser()
        article = parser.parse(raw_content)
        return article.content

    def _extract_with_boilerpy3(self, raw_content: str) -> str:
        """
        Extract text using the boilerpy3 library.

        Args:
            raw_content (str): The raw HTML content.

        Returns:
            str: The extracted content.
        """
        from boilerpy3 import extractors
        extractor = extractors.ArticleExtractor()
        return extractor.get_content(raw_content)

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

    def _extract_with_newspaper(self, raw_content: str) -> str:
        """
        Extract text using the newspaper library.

        Args:
            raw_content (str): The raw HTML content.

        Returns:
            str: The extracted text.
        """
        from newspaper import Article
        article = Article('')
        article.set_html(raw_content)
        article.parse()
        return article.text

    def _extract_with_goose(self, raw_content: str) -> str:
        """
        Extract text using the goose3 library.

        Args:
            raw_content (str): The raw HTML content.

        Returns:
            str: The extracted text.
        """
        from goose3 import Goose
        g = Goose()
        article = g.extract(raw_html=raw_content)
        return article.cleaned_text

    @staticmethod
    def _remove_urls(content: str) -> str:
        """
        Remove URLs from the given content using regex.

        Args:
            content (str): The content to process.

        Returns:
            str: The content with URLs removed.
        """

        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        return url_pattern.sub('', content)

    @staticmethod
    def _extract_metadata(content: str) -> Dict[str, Any]:
        """
        Extract basic metadata from the processed content.

        Args:
            content (str): The processed content.

        Returns:
            Dict[str, Any]: A dictionary containing extracted metadata.
        """

        metadata = {}
        lines = content.split('\n')
        title = next((line for line in lines if line.strip()), '')
        metadata['title'] = title
        words = re.findall(r'\w+', content)
        metadata['word_count'] = len(words)
        metadata['estimated_read_time'] = round(len(words) / 200)
        return metadata
import requests
from bs4 import BeautifulSoup
import re
from ct.abstracts import AbstractWebParser
from ct.interfaces import IProcessor
from typing import Dict, List

try:
    import newspaper
    from goose3 import Goose
    EXTRA_LIBRARIES_AVAILABLE = True
except ImportError:
    EXTRA_LIBRARIES_AVAILABLE = False

__All__ = ['WebParser']


class WebParser(AbstractWebParser):
    def __init__(self, processor: IProcessor, url: str, method: str = 'custom'):
        super().__init__(processor, url)
        self.method = method
        if method in ['newspaper', 'goose'] and not EXTRA_LIBRARIES_AVAILABLE:
            raise ImportError(f"The {method} library is not installed. Please install it to use this method.")

    def fetch_content(self, url: str) -> str:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.text

    def extract_text(self, raw_content: str) -> str:
        if self.method == 'newspaper':
            return self._extract_with_newspaper()
        elif self.method == 'goose':
            return self._extract_with_goose()
        elif self.method == 'raw':
            return self.extract_raw(raw_content)
        else:
            return self._extract_custom(raw_content)

    def extract_raw(self, raw_content: str) -> str:
        soup = BeautifulSoup(raw_content, 'html.parser')
        return soup.get_text()

    def _extract_custom(self, raw_content: str) -> str:
        soup = BeautifulSoup(raw_content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Look for common article container classes or IDs
        article = soup.find('article') or soup.find('div', class_=re.compile('article|content|post'))

        if article:
            # If we found an article container, use its text
            text = article.get_text()
        else:
            # Fallback: use the text from the body, excluding common non-content areas
            for elem in soup(['header', 'nav', 'footer', 'aside']):
                elem.decompose()
            text = soup.body.get_text()

        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return text

    def _extract_with_newspaper(self) -> str:
        article = newspaper.Article(self.url)
        article.download()
        article.parse()
        return article.text

    def _extract_with_goose(self) -> str:
        g = Goose()
        article = g.extract(url=self.url)
        return article.cleaned_text

    def parse(self) -> Dict[str, List[str]]:
        """Parse the content from the given URL."""
        raw_content = self.fetch_content(self.url)
        text = self.extract_text(raw_content)
        processed_text = self.processor.process(text)
        return {"web_content": processed_text}
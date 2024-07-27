import requests
from bs4 import BeautifulSoup
import re
from ct.abstracts import AbstractWebParser
from ct.interfaces import IProcessor
from typing import Dict, List

__All__ = ['WebParser']


class WebParser(AbstractWebParser):
    def __init__(self, processor: IProcessor, url: str, method: str = 'custom'):
        super().__init__(processor, url)
        self.method = method
        self._check_dependencies()

    def _check_dependencies(self):
        self.available_methods = ['custom', 'raw']
        try:
            # Best method for extracting content from web pages
            import trafilatura
            self.available_methods.append('traf')
        except ImportError:
            pass
        try:
            from readability import Document
            self.available_methods.append('readability')
        except ImportError:
            pass
        try:
            from article_parser import ArticleParser
            self.available_methods.append('article_parser')
        except ImportError:
            pass
        try:
            # TODO: gives a "urllib.error.HTTPError: HTTP Error 403: Forbidden" error
            from boilerpy3 import extractors
            self.available_methods.append('boilerpy3')
        except ImportError:
            pass
        try:
            import html2text
            self.available_methods.append('html2text')
        except ImportError:
            pass
        try:
            import newspaper
            self.available_methods.append('newspaper')
        except ImportError:
            pass
        try:
            from goose3 import Goose
            self.available_methods.append('goose')
        except ImportError:
            pass

        if self.method not in self.available_methods:
            raise ImportError(f"The {self.method} method is not available. Please install the required library.")

    def fetch_content(self, url: str) -> str:
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    def extract_text(self, raw_content: str) -> str:
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
        soup = BeautifulSoup(raw_content, 'html.parser')
        return soup.get_text()

    def _extract_custom(self, raw_content: str) -> str:
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
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return text

    def _extract_with_trafilatura(self, raw_content: str) -> str:
        import trafilatura
        return trafilatura.extract(raw_content) or ''

    def _extract_with_readability(self, raw_content: str) -> str:
        from readability import Document
        doc = Document(raw_content)
        return doc.summary()

    def _extract_with_article_parser(self) -> str:
        from article_parser import ArticleParser
        parser = ArticleParser()
        article = parser.parse(self.url)
        return article.content

    def _extract_with_boilerpy3(self) -> str:
        from boilerpy3 import extractors
        extractor = extractors.ArticleExtractor()
        return extractor.get_content_from_url(self.url)

    def _extract_with_html2text(self, raw_content: str) -> str:
        import html2text
        h = html2text.HTML2Text()
        h.ignore_links = True
        return h.handle(raw_content)

    def _extract_with_newspaper(self) -> str:
        import newspaper
        article = newspaper.article(self.url)
        article.download()
        article.parse()
        return article.text

    def _extract_with_goose(self) -> str:
        from goose3 import Goose
        g = Goose()
        article = g.extract(url=self.url)
        return article.cleaned_text

    def parse(self) -> Dict[str, List[str]]:
        """Parse the content from the given URL."""
        raw_content = self.fetch_content(self.url)
        text = self.extract_text(raw_content)
        processed_text = self.processor.process(text)
        return {"web_content": processed_text}

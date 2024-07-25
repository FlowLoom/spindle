from abc import abstractmethod
from typing import Any, Dict, List
from ct.interfaces import IProcessor, IParser

__All__ = ['AbstractWebParser']


class AbstractWebParser(IParser):
    def __init__(self, processor: IProcessor, url: str):
        self.processor = processor
        self.url = url

    @abstractmethod
    def fetch_content(self, url: str) -> str:
        """Fetch the raw content from the given URL."""
        pass

    @abstractmethod
    def extract_text(self, raw_content: str) -> str:
        """Extract the relevant text from the raw content."""
        pass

    def parse(self) -> Dict[str, List[str]]:
        """Parse the content from the given URL."""
        raw_content = self.fetch_content(self.url)
        text = self.extract_text(raw_content)
        processed_text = self.processor.process(text)
        return {"web_content": processed_text}

from spindle.interfaces import IProcessor
from typing import List

__All__ = ['WebProcessor']


class WebProcessor(IProcessor):
    def process(self, content: str) -> List[str]:
        # Split the content into lines and remove empty lines
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        return lines

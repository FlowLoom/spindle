from spindle.interfaces import IParser, IVisitor
from typing import Dict, List

__All__ = ['CompositeParser']


class CompositeParser(IParser):
    def __init__(self):
        self.parsers = []

    def accept(self, visitor):
        for parser in self.parsers:
            parser.accept(visitor)

    def add(self, parser):
        self.parsers.append(parser)

    def remove(self, parser):
        self.parsers.remove(parser)

    def parse(self) -> Dict[str, List[str]]:
        result = {}
        for parser in self.parsers:
            result.update(parser.parse())
        return result

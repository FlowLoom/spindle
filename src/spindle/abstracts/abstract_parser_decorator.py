from spindle.interfaces import IParser
from typing import Dict, List

__All__ = ["AbstractParserDecorator"]


class AbstractParserDecorator(IParser):
    def __init__(self, wrapped_parser: IParser):
        self.wrapped_parser = wrapped_parser

    def parse(self) -> Dict[str, List[str]]:
        return self.wrapped_parser.parse()

    def accept(self, visitor):
        self.wrapped_parser.accept(visitor)
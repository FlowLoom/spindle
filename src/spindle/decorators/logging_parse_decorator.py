from spindle.abstracts import AbstractParserDecorator
from typing import Dict, List

__All__ = ["LoggingParserDecorator"]


class LoggingParserDecorator(AbstractParserDecorator):
    def parse(self) -> Dict[str, List[str]]:
        print(f"Starting parsing with {self.wrapped_parser.__class__.__name__}")
        result = super().parse()
        print(f"Finished parsing with {self.wrapped_parser.__class__.__name__}")
        return result
from typing import Dict, List
from spindle.abstracts import AbstractParserDecorator
import time

__All__ = ["TimingParserDecorator"]


class TimingParserDecorator(AbstractParserDecorator):
    def parse(self) -> Dict[str, List[str]]:
        start_time = time.time()
        result = super().parse()
        end_time = time.time()
        print(f"Parsing with {self.wrapped_parser.__class__.__name__} took {end_time - start_time:.2f} seconds")
        return result

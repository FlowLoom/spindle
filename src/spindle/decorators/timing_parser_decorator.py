from typing import Dict, List
from spindle.abstracts import AbstractParserDecorator
import time

__All__ = ["TimingParserDecorator"]


class TimingParserDecorator(AbstractParserDecorator):
    """
    A decorator class that adds timing functionality to a parser.

    This class wraps another parser and measures the time taken to execute
    its parse method. It inherits from AbstractParserDecorator.
    """
    def parse(self) -> Dict[str, List[str]]:
        """
        Execute the parse method of the wrapped parser and measure its execution time.

        Returns:
            Dict[str, List[str]]: The result of the wrapped parser's parse method.

        Side Effects:
            Prints the execution time of the wrapped parser's parse method to the console.
        """
        start_time = time.time()
        result = super().parse()
        end_time = time.time()
        print(f"Parsing with {self.wrapped_parser.__class__.__name__} took {end_time - start_time:.2f} seconds")
        return result

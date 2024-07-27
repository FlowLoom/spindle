from spindle.abstracts import AbstractParserDecorator
from typing import Dict, List

__All__ = ["LoggingParserDecorator"]


class LoggingParserDecorator(AbstractParserDecorator):
    """
    A decorator class that adds logging functionality to a parser.

    This class extends AbstractParserDecorator to provide logging before and after
    the parsing process.
    """

    def parse(self) -> Dict[str, List[str]]:
        """
        Execute the parsing process with added logging.

        This method wraps the parse method of the decorated parser with log messages
        indicating the start and end of the parsing process.

        Returns:
            Dict[str, List[str]]: The result of the parsing process.

        Side Effects:
            Prints the prints the start and end of the wrapped parser's class name to the console.
        """
        print(f"Starting parsing with {self.wrapped_parser.__class__.__name__}")
        result = super().parse()
        print(f"Finished parsing with {self.wrapped_parser.__class__.__name__}")
        return result
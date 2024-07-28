from spindle.abstracts import AbstractFetcherDecorator
from typing import Dict, List

__All__ = ["LoggingFetcherDecorator"]


class LoggingFetcherDecorator(AbstractFetcherDecorator):
    """
    A decorator class that adds logging functionality to a fetcher.

    This class extends AbstractParserDecorator to provide logging before and after
    the fetching process.
    """

    def fetch(self) -> Dict[str, List[str]]:
        """
        Execute the fetch process with added logging.

        This method wraps the fetch method of the decorated fetcher with log messages
        indicating the start and end of the fetching process.

        Returns:
            Dict[str, List[str]]: The result of the fetching process.

        Side Effects:
            Prints the prints the start and end of the wrapped fetcher's class name to the console.
        """
        print(f"Starting fetching with {self.wrapped_fetcher.__class__.__name__}")
        result = super().fetch()
        print(f"Finished fetching with {self.wrapped_fetcher.__class__.__name__}")
        return result
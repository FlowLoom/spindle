from typing import Dict, List
from spindle.abstracts import AbstractFetcherDecorator
import time

__All__ = ["TimingFetcherDecorator"]


class TimingFetcherDecorator(AbstractFetcherDecorator):
    """
    A decorator class that adds timing functionality to a fetcher.

    This class wraps another fetcher and measures the time taken to execute
    its fetch method. It inherits from AbstractFetchDecorator.
    """
    def fetch(self) -> Dict[str, List[str]]:
        """
        Execute the fetch method of the wrapped fetcher and measure its execution time.

        Returns:
            Dict[str, List[str]]: The result of the wrapped fetcher's parse method.

        Side Effects:
            Prints the execution time of the wrapped fetchers's fetch method to the console.
        """
        start_time = time.time()
        result = super().parse()
        end_time = time.time()
        print(f"Parsing with {self.wrapped_fetcher.__class__.__name__} took {end_time - start_time:.2f} seconds")
        return result

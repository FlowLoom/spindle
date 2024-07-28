from typing import Dict, List, Any, Type, Callable
from spindle.interfaces import IFetcher, IProcessor, IVisitor
import time

__All__ = ["TimingFetcherDecorator", "timing_fetcher_decorator"]


class TimingFetcherDecorator(IFetcher):
    """
    A decorator class that adds timing functionality to a fetcher.

    This class wraps another fetcher and measures the time taken to execute
    its fetch method. It inherits from AbstractFetchDecorator.
    """

    def __init__(self, fetcher: IFetcher):
        self.fetcher = fetcher

    @property
    def processor(self) -> IProcessor:
        return self.fetcher.processor

    def fetch(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """
        Execute the fetch method of the wrapped fetcher and measure its execution time.

        Returns:
            Dict[str, List[str]]: The result of the wrapped fetcher's parse method.

        Side Effects:
            Prints the execution time of the wrapped fetchers's fetch method to the console.
        """
        start_time = time.time()
        result = self.fetcher.fetch(*args, **kwargs)
        end_time = time.time()
        print(f"Parsing with {self.fetcher.__class__.__name__} took {end_time - start_time:.2f} seconds")
        return result

    def _fetch_content(self, source: Any) -> Any:
        return self.fetcher._fetch_content(*args, **kwargs)

    def _process_content(self, content: Any) -> Any:
        return self.fetcher._process_content(*args, **kwargs)

    def _format_output(self, processed_content: Any) -> Dict[str, Any]:
        return self.fetcher._format_output(processed_content)

    def accept(self, visitor: IVisitor) -> None:
        self.fetcher.accept(visitor)


def timing_fetcher_decorator(cls: Type[IFetcher]) -> Callable[..., TimingFetcherDecorator]:
    """
    A decorator function that wraps a fetcher class with LoggingFetcher.

    Args:
        cls (Type[IFetcher]): The fetcher class to be decorated.

    Returns:
        Callable[..., LoggingFetcher]: A function that creates a LoggingFetcher instance.
    """
    def wrapper(*args: Any, **kwargs: Any) -> TimingFetcherDecorator:
        return TimingFetcherDecorator(cls(*args, **kwargs))
    return wrapper
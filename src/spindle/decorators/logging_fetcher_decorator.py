from typing import Any, Dict, Type, Callable
from spindle.interfaces import IFetcher, IProcessor, IVisitor

__ALL__ = ["LoggingFetcherDecorator", "logging_fetcher_decorator"]


class LoggingFetcherDecorator(IFetcher):
    """
    A decorator class that adds logging functionality to a fetcher.
    This class implements the IFetcher interface and wraps another IFetcher instance.
    """

    def __init__(self, fetcher: IFetcher):
        self.fetcher = fetcher

    @property
    def processor(self) -> IProcessor:
        return self.fetcher.processor

    def fetch(self, source: Any) -> Dict[str, Any]:
        """
        Execute the fetch process with added logging.

        Args:
            source (Any): The source to fetch from.

        Returns:
            Dict[str, Any]: The result of the fetching process.

        Side Effects:
            Prints the start and end of the wrapped fetcher's class name to the console.
        """
        print(f"Starting fetching with {self.fetcher.__class__.__name__}")
        result = self.fetcher.fetch(source)
        print(f"Finished fetching with {self.fetcher.__class__.__name__}")
        return result

    def _fetch_content(self, source: Any) -> Any:
        return self.fetcher._fetch_content(source)

    def _process_content(self, content: Any) -> Any:
        return self.fetcher._process_content(content)

    def _format_output(self, processed_content: Any) -> Dict[str, Any]:
        return self.fetcher._format_output(processed_content)

    def accept(self, visitor: IVisitor) -> None:
        self.fetcher.accept(visitor)


def logging_fetcher_decorator(cls: Type[IFetcher]) -> Callable[..., LoggingFetcherDecorator]:
    """
    A decorator function that wraps a fetcher class with LoggingFetcher.

    Args:
        cls (Type[IFetcher]): The fetcher class to be decorated.

    Returns:
        Callable[..., LoggingFetcher]: A function that creates a LoggingFetcher instance.
    """
    def wrapper(*args: Any, **kwargs: Any) -> LoggingFetcher:
        return LoggingFetcherDecorator(cls(*args, **kwargs))
    return wrapper
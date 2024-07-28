from spindle.abstracts import AbstractFetcherFactory
from spindle.fetchers import WebFetcher
from spindle.processors import WebProcessor
from spindle.handlers import FileHandler, ConsoleHandler
from spindle.interfaces import IHandler, IProcessor, IFetcher
from typing import Any

__ALL__ = ['WebFetcherFactory']


class WebFetcherFactory(AbstractFetcherFactory):
    """
    A factory class for creating web fetcher components.

    This class extends AbstractFetcherFactory to provide specific implementations
    for web fetcher, including methods to create fetchering, processors, and handlers.
    It also allows configuration of default values for various fetching parameters.
    """

    def __init__(self):
        """
        Initialize the WebFetchFactory with default configuration values.
        """

        self.default_extraction_method = 'custom'
        self.default_remove_html = True
        self.default_remove_excess_whitespace = True
        self.default_remove_urls = False
        self.default_min_line_length = 0
        self.default_max_line_length = None
        self.default_extract_metadata = False

    def _create_fetcher(self, *args, **kwargs) -> IFetcher:
        """
        Create and return a WebFetcher instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            WebParser: An instance of WebParser.
        """
        processor = self._create_processor(**kwargs)
        return WebFetcher(processor)

    def _create_processor(self, **kwargs) -> IProcessor:
        """
        Create and return a WebProcessor instance.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            IProcessor: An instance of WebProcessor.
        """
        return WebProcessor(
            extraction_method=kwargs.get('extraction_method', self.default_extraction_method),
            remove_html=kwargs.get('remove_html', self.default_remove_html),
            remove_excess_whitespace=kwargs.get('remove_excess_whitespace', self.default_remove_excess_whitespace),
            remove_urls=kwargs.get('remove_urls', self.default_remove_urls),
            min_line_length=kwargs.get('min_line_length', self.default_min_line_length),
            max_line_length=kwargs.get('max_line_length', self.default_max_line_length),
            extract_metadata=kwargs.get('extract_metadata', self.default_extract_metadata)
        )

    def _create_handler(self, *args, **kwargs) -> IHandler:
        """
        Create and return an appropriate handler instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            IHandler: An instance of a concrete handler (ConsolePrintHandler or FileHandler)
                      based on the provided arguments.
        """

        if kwargs.get('console') or kwargs.get('con'):
            return ConsolePrintHandler()
        elif 'output' in kwargs and kwargs['output'] is not None:
            return FileHandler(kwargs['output'])
        else:
            return ConsolePrintHandler()

    def set_default_extraction_method(self, method: str) -> None:
        """
        Set the default extraction method for the WebProcessor.

        Args:
            method (str): The extraction method to use by default.
        """
        self.default_extraction_method = method

    def set_default_remove_html(self, remove: bool) -> None:
        """
        Set whether to remove HTML tags by default.

        Args:
            remove (bool): Whether to remove HTML tags.
        """
        self.default_remove_html = remove

    def set_default_remove_excess_whitespace(self, remove: bool) -> None:
        """
        Set whether to remove excess whitespace by default.

        Args:
            remove (bool): Whether to remove excess whitespace.
        """
        self.default_remove_excess_whitespace = remove

    def set_default_remove_urls(self, remove: bool) -> None:
        """
        Set whether to remove URLs by default.

        Args:
            remove (bool): Whether to remove URLs.
        """
        self.default_remove_urls = remove

    def set_default_min_line_length(self, length: int) -> None:
        """
        Set the default minimum line length.

        Args:
            length (int): The minimum line length to use by default.
        """
        self.default_min_line_length = length

    def set_default_max_line_length(self, length: int) -> None:
        """
        Set the default maximum line length.

        Args:
            length (int): The maximum line length to use by default.
        """
        self.default_max_line_length = length

    def set_default_extract_metadata(self, extract: bool) -> None:
        """
        Set whether to extract metadata by default.

        Args:
            extract (bool): Whether to extract metadata.
        """
        self.default_extract_metadata = extract

    def create_fetcher(self, *args: Any, **kwargs: Any) -> WebFetcher:
        """
        Create and return a WebFetcher instance.

        This method overrides the abstract method in the base class to provide
        a more specific return type hint.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            WebParser: An instance of WebFetcher.
        """
        return super().create_fetcher(*args, **kwargs)

    def create_processor(self, *args: Any, **kwargs: Any) -> WebProcessor:
        """
        Create and return a WebProcessor instance.

        This method overrides the abstract method in the base class to provide
        a more specific return type hint.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            WebProcessor: An instance of WebProcessor.
        """
        return super().create_processor(*args, **kwargs)

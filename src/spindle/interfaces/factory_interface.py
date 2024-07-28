# TODO: Rename module to fetcher_factory_interface.py
from abc import ABC, abstractmethod
from spindle.interfaces import IFetcher, IProcessor, IHandler

__All__ = ['IFetcherFactory']

# TODO: Add private methods to the interface
class IFetcherFactory(ABC):
    """
    Abstract base class defining the interface for a parser factory.

    This factory is responsible for creating parsers, processors, and handlers.
    """

    @abstractmethod
    def create_fetcher(self, *args, **kwargs) -> IFetcher:
        """
        Create and return a fetcher object.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            IParser: An instance of a class implementing the IParser interface.
        """
        pass

    @abstractmethod
    def create_processor(self, *args, **kwargs) -> IProcessor:
        """
        Create and return a processor object.

        Returns:
            IProcessor: An instance of a class implementing the IProcessor interface.
        """
        pass

    @abstractmethod
    def create_handler(self, *args, **kwargs) -> IHandler:
        """
        Create and return a handler object.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            IHandler: An instance of a class implementing the IHandler interface.
        """
        pass

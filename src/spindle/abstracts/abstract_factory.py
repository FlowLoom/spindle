from spindle.interfaces import IFetcherFactory
from spindle.interfaces import IFetcher
from spindle.interfaces import IProcessor
from spindle.interfaces import IHandler
from abc import abstractmethod

__All__ = ['AbstractFetcherFactory']


class AbstractFetcherFactory(IFetcherFactory):
    def create_fetcher(self, *args, **kwargs) -> IFetcher:
        fetcher = self._create_fetcher(*args, **kwargs)
        return fetcher

    def create_processor(self, *args, **kwargs) -> IProcessor:
        processor = self._create_processor(*args, **kwargs)
        return processor

    def create_handler(self, *args, **kwargs) -> IHandler:
        handler = self._create_handler(*args, **kwargs)
        return handler

    @abstractmethod
    def _create_fetcher(self, *args, **kwargs) -> IFetcher:
        pass

    @abstractmethod
    def _create_processor(self, *args, **kwargs) -> IProcessor:
        pass

    @abstractmethod
    def _create_handler(self, *args, **kwargs) -> IHandler:
        pass

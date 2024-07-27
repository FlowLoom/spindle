from abc import ABC, abstractmethod
from ct.interfaces import IParser, IProcessor, IHandler

__All__ = ['IParserFactory']


class IParserFactory(ABC):
    @abstractmethod
    def create_parser(self, *args, **kwargs) -> IParser:
        pass

    @abstractmethod
    def create_processor(self) -> IProcessor:
        pass

    @abstractmethod
    def create_handler(self, *args, **kwargs) -> IHandler:
        pass
from abc import ABC, abstractmethod
from typing import Type, List
from spindle.interfaces import IProcessor, IParser, IHandler

__All__ = ["ICerebro"]


class ICerebro(ABC):
    @abstractmethod
    def add_processor(self, processor: Type[IProcessor]) -> None:
        pass

    @abstractmethod
    def add_parser(self, parser: Type[IParser]) -> None:
        pass

    @abstractmethod
    def add_handler(self, handler: Type[IHandler]) -> None:
        pass

    @abstractmethod
    def run(self, *args, **kwargs) -> None:
        pass

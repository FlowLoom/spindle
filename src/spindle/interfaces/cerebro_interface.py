from abc import ABC, abstractmethod
from typing import Type, List
from spindle.interfaces import IProcessor, IParser, IHandler

__All__ = ["ICerebro"]


class ICerebro(ABC):
    """
    Abstract base class defining the interface for a Cerebro component.

    This class provides a blueprint for implementing a Cerebro system,
    which can manage processors, parsers, and handlers.
    """

    @abstractmethod
    def add_processor(self, processor: Type[IProcessor]) -> None:
        """
        Add a processor to the Cerebro system.

        Args:
            processor (Type[IProcessor]): The processor class to be added.

        Returns:
            None
        """
        pass

    @abstractmethod
    def add_parser(self, parser: Type[IParser]) -> None:
        """
        Add a parser to the Cerebro system.

        Args:
            parser (Type[IParser]): The parser class to be added.

        Returns:
            None
        """
        pass

    @abstractmethod
    def add_handler(self, handler: Type[IHandler]) -> None:
        """
        Add a handler to the Cerebro system.

        Args:
            handler (Type[IHandler]): The handler class to be added.

        Returns:
            None
        """
        pass

    @abstractmethod
    def run(self, *args, **kwargs) -> None:
        """
        Execute the Cerebro system with the configured components.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """
        pass

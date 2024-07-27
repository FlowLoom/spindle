from spindle.abstracts.abstract_factory import AbstractParserFactory
from spindle.parsers import WebParser
from spindle.processors import WebProcessor
from spindle.handlers import FileHandler

__All__ = ['WebParserFactory']


class WebParserFactory(AbstractParserFactory):
    """
    A concrete factory for creating web parsing components.

    This factory implements the AbstractParserFactory interface to create
    specific instances of parser, processor, and handler for web parsing.
    """
    def _create_concrete_parser(self, *args, **kwargs) -> WebParser:
        """
        Create and return a WebParser instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            WebParser: An instance of WebParser with an associated processor.
        """
        return WebParser(self.create_processor(), *args, **kwargs)

    def _create_concrete_processor(self) -> WebProcessor:
        """
        Create and return a WebProcessor instance.

        Returns:
            WebProcessor: An instance of WebProcessor.
        """
        return WebProcessor()

    def _create_concrete_handler(self, *args, **kwargs) -> FileHandler:
        """
        Create and return a FileHandler instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            FileHandler: An instance of FileHandler.
        """
        return FileHandler(*args, **kwargs)

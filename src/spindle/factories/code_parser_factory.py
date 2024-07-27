from spindle.abstracts.abstract_factory import AbstractParserFactory
from spindle.parsers import CodeParser
from spindle.processors import FileProcessor
from spindle.handlers import FileHandler, ConsolePrintHandler
from spindle.interfaces import IHandler

__All__ = ['CodeParserFactory']


class CodeParserFactory(AbstractParserFactory):
    """
    A factory class for creating code parsing components.

    This class implements the Abstract Factory pattern to create concrete instances
    of parsers, processors, and handlers for code parsing operations.
    """

    def _create_concrete_parser(self, *args, **kwargs) -> CodeParser:
        """
        Create a concrete CodeParser instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            CodeParser: An instance of CodeParser with the created processor.
        """
        return CodeParser(self.create_processor(), *args, **kwargs)

    def _create_concrete_processor(self) -> FileProcessor:
        """
        Create a concrete FileProcessor instance.

        Returns:
            FileProcessor: An instance of FileProcessor.
        """
        return FileProcessor()

    def _create_concrete_handler(self, *args, **kwargs) -> IHandler:
        """
        Create a concrete handler based on the provided arguments.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            IHandler: An instance of a concrete handler (ConsolePrintHandler or FileHandler).
        """

        # Check if 'console' or 'con' flag is present in kwargs
        if kwargs.get('console') or kwargs.get('con'):
            return ConsolePrintHandler()

        # Check if 'output' is provided in kwargs
        elif 'output' in kwargs:
            return FileHandler(kwargs['output'])

        # If no specific arguments are provided, default to ConsolePrintHandler
        else:
            return ConsolePrintHandler()


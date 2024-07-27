from spindle.abstracts.abstract_factory import AbstractParserFactory
from spindle.parsers import CodeParser
from spindle.processors import FileProcessor
from spindle.handlers import FileHandler, ConsolePrintHandler
from spindle.interfaces import IHandler

__All__ = ['CodeParserFactory']


class CodeParserFactory(AbstractParserFactory):
    def _create_concrete_parser(self, *args, **kwargs) -> CodeParser:
        return CodeParser(self.create_processor(), *args, **kwargs)

    def _create_concrete_processor(self) -> FileProcessor:
        return FileProcessor()

    def _create_concrete_handler(self, *args, **kwargs) -> IHandler:
        # Check if 'console' or 'con' flag is present in kwargs
        if kwargs.get('console') or kwargs.get('con'):
            return ConsolePrintHandler()

        # Check if 'output' is provided in kwargs
        elif 'output' in kwargs:
            return FileHandler(kwargs['output'])

        # If no specific arguments are provided, default to ConsolePrintHandler
        else:
            return ConsolePrintHandler()


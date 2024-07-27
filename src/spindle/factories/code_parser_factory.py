from spindle.abstracts.abstract_factory import AbstractParserFactory
from spindle.parsers import CodeParser
from spindle.processors import FileProcessor
from spindle.handlers import FileHandler

__All__ = ['CodeParserFactory']


class CodeParserFactory(AbstractParserFactory):
    def _create_concrete_parser(self, *args, **kwargs) -> CodeParser:
        return CodeParser(self.create_processor(), *args, **kwargs)

    def _create_concrete_processor(self) -> FileProcessor:
        return FileProcessor()

    def _create_concrete_handler(self, *args, **kwargs) -> FileHandler:
        return FileHandler(*args, **kwargs)


from spindle.abstracts.abstract_factory import AbstractParserFactory
from spindle.parsers import WebParser
from spindle.processors import WebProcessor
from spindle.handlers import FileHandler

__All__ = ['WebParserFactory']


class WebParserFactory(AbstractParserFactory):
    def _create_concrete_parser(self, *args, **kwargs) -> WebParser:
        return WebParser(self.create_processor(), *args, **kwargs)

    def _create_concrete_processor(self) -> WebProcessor:
        return WebProcessor()

    def _create_concrete_handler(self, *args, **kwargs) -> FileHandler:
        return FileHandler(*args, **kwargs)

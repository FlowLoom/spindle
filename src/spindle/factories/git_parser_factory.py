from spindle.abstracts.abstract_factory import AbstractParserFactory
from spindle.parsers import GitCommitParser
from spindle.processors import DummyProcessor
from spindle.handlers import ConsolePrintHandler

__All__ = ['GitParserFactory']


class GitParserFactory(AbstractParserFactory):
    def _create_concrete_parser(self, *args, **kwargs) -> GitCommitParser:
        return GitCommitParser(self.create_processor(), *args, **kwargs)

    def _create_concrete_processor(self) -> DummyProcessor:
        return DummyProcessor()

    def _create_concrete_handler(self, *args, **kwargs) -> ConsolePrintHandler:
        return ConsolePrintHandler()


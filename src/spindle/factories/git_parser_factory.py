from spindle.abstracts.abstract_factory import AbstractParserFactory
from spindle.parsers import GitCommitParser
from spindle.processors import DummyProcessor
from spindle.handlers import ConsolePrintHandler

__All__ = ['GitParserFactory']


class GitParserFactory(AbstractParserFactory):
    """
    A concrete factory for creating Git-related parsing components.

    This factory implements the AbstractParserFactory interface to create
    specific instances of parser, processor, and handler for Git operations.
    """
    def _create_concrete_parser(self, *args, **kwargs) -> GitCommitParser:
        """
        Create and return a GitCommitParser instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            GitCommitParser: An instance of GitCommitParser with the created processor.
        """
        return GitCommitParser(self.create_processor(), *args, **kwargs)

    def _create_concrete_processor(self) -> DummyProcessor:
        """
        Create and return a DummyProcessor instance.

        Returns:
            DummyProcessor: An instance of DummyProcessor.
        """
        return DummyProcessor()

    def _create_concrete_handler(self, *args, **kwargs) -> ConsolePrintHandler:
        """
        Create and return a ConsolePrintHandler instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            ConsolePrintHandler: An instance of ConsolePrintHandler.
        """
        return ConsolePrintHandler()


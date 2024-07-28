from spindle.abstracts import AbstractFetcherFactory
from spindle.fetchers import GitCommitFetcher
from spindle.processors import GitCommitProcessor
from spindle.handlers import FileHandler, ConsolePrintHandler
from spindle.interfaces import IHandler, IProcessor, IFetcher

__All__ = ['GitFetcherFactory']


class GitFetcherFactory(AbstractFetcherFactory):
    def __init__(self):
        self.default_extract_ticket_number = False
        self.default_max_length = 72
        self.default_capitalize_first_word = True

    def _create_fetcher(self, *args, **kwargs) -> IFetcher:
        """
        Create and return a GitCommitParser instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            GitCommitParser: An instance of GitCommitParser.
        """
        processor = self._create_processor(**kwargs)
        return GitCommitFetcher(processor)

    def _create_processor(self, **kwargs) -> IProcessor:
        """
        Create and return a GitCommitProcessor instance.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            IProcessor: An instance of GitCommitProcessor.
        """
        extract_ticket_number = kwargs.get('extract_ticket_number', self.default_extract_ticket_number)
        max_length = kwargs.get('max_length', self.default_max_length)
        capitalize_first_word = kwargs.get('capitalize_first_word', self.default_capitalize_first_word)

        return GitCommitProcessor(
            extract_ticket_number=extract_ticket_number,
            max_length=max_length,
            capitalize_first_word=capitalize_first_word
        )

    def _create_handler(self, *args, **kwargs) -> IHandler:
        """
        Create and return an appropriate handler instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            IHandler: An instance of a concrete handler (ConsolePrintHandler or FileHandler)
                      based on the provided arguments.
        """

        if kwargs.get('console') or kwargs.get('con'):
            return ConsolePrintHandler()
        elif 'output' in kwargs and kwargs['output'] is not None:
            return FileHandler(kwargs['output'])
        else:
            return ConsolePrintHandler()

    def set_default_extract_ticket_number(self, extract: bool) -> None:
        """
        Set the default value for extracting ticket numbers.

        Args:
            extract (bool): Whether to extract ticket numbers by default.
        """
        self.default_extract_ticket_number = extract

    def set_default_max_length(self, length: int) -> None:
        """
        Set the default maximum length for commit messages.

        Args:
            length (int): The default maximum length.
        """
        self.default_max_length = length

    def set_default_capitalize_first_word(self, capitalize: bool) -> None:
        """
        Set the default value for capitalizing the first word.

        Args:
            capitalize (bool): Whether to capitalize the first word by default.
        """
        self.default_capitalize_first_word = capitalize
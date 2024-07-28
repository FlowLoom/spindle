from spindle.fetchers import GitCommitFetcher
from spindle.processors import GitCommitProcessor
from spindle.handlers import FileHandler, ConsoleHandler, CompositeHandler, Color
from spindle.serializers import ISerializer
from .serializer_factory import SerializerFactory
from spindle.decorators import TimingFetcherDecorator
from spindle.abstracts import AbstractFetcherFactory
from spindle.interfaces import IHandler, IFetcher
from typing import List, Optional

__All__ = ['GitFetcherFactory']


class GitFetcherFactory(AbstractFetcherFactory):
    def __init__(self):
        self.default_extract_ticket_number = False
        self.default_max_length = -1
        self.default_capitalize_first_word = True
        self.serializer_factory = SerializerFactory()

    def _create_fetcher(self, stats: bool = False, **kwargs) -> IFetcher:
        processor = self._create_processor(**kwargs)
        fetcher = GitCommitFetcher(processor)
        if stats:
            fetcher = TimingFetcherDecorator(fetcher)
        return fetcher

    def _create_handler(self, output: Optional[str], format: str = 'plaintext', color: Optional[str] = None) -> IHandler:
        serializer = self.serializer_factory.create_serializer(format)
        handlers = []

        if output:
            file_handler = FileHandler(serializer, output)
            handlers.append(file_handler)

        console_handler = ConsoleHandler(serializer)
        if color:
            console_handler.set_color(Color[color.upper()])
        handlers.append(console_handler)

        if len(handlers) > 1:
            composite_handler = CompositeHandler()
            for handler in handlers:
                composite_handler.add_handler(handler)
            return composite_handler
        else:
            return handlers[0]

    def _create_processor(self, **kwargs) -> GitCommitProcessor:
        return GitCommitProcessor(
            extract_ticket_number=kwargs.get('extract_ticket_number', self.default_extract_ticket_number),
            max_length=kwargs.get('max_length', self.default_max_length),
            capitalize_first_word=kwargs.get('capitalize_first_word', self.default_capitalize_first_word)
        )

    def set_default_extract_ticket_number(self, extract: bool) -> None:
        self.default_extract_ticket_number = extract

    def set_default_max_length(self, length: int) -> None:
        self.default_max_length = length

    def set_default_capitalize_first_word(self, capitalize: bool) -> None:
        self.default_capitalize_first_word = capitalize
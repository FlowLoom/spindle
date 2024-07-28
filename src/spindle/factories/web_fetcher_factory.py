from spindle.abstracts import AbstractFetcherFactory
from spindle.fetchers import WebFetcher
from spindle.processors import WebProcessor
from spindle.handlers import FileHandler, ConsoleHandler
from spindle.serializers import ISerializer
from spindle.factories import SerializerFactory
from spindle.interfaces import IHandler, IFetcher
from typing import Optional

__All__ = ['WebFetcherFactory']


class WebFetcherFactory(AbstractFetcherFactory):
    def __init__(self):
        self.default_extraction_method = 'custom'
        self.default_remove_html = True
        self.default_remove_excess_whitespace = True
        self.default_remove_urls = False
        self.default_min_line_length = 0
        self.default_max_line_length = None
        self.default_extract_metadata = False
        self.serializer_factory = SerializerFactory()

    def _create_fetcher(self, **kwargs) -> IFetcher:
        processor = self._create_processor(**kwargs)
        return WebFetcher(processor)

    def _create_handler(self, handler_type: str, format: str = 'plaintext', **kwargs) -> IHandler:
        serializer = self.serializer_factory.create_serializer(format)

        if handler_type.lower() == 'file':
            return FileHandler(serializer, kwargs.get('output_file', 'output.txt'))
        elif handler_type.lower() == 'console':
            console_handler = ConsoleHandler(serializer)
            if 'color' in kwargs:
                console_handler.set_color(kwargs['color'])
            return console_handler
        else:
            raise ValueError(f"Unsupported handler type: {handler_type}")

    def _create_processor(self, **kwargs) -> WebProcessor:
        return WebProcessor(
            extraction_method=kwargs.get('extraction_method', self.default_extraction_method),
            remove_html=kwargs.get('remove_html', self.default_remove_html),
            remove_excess_whitespace=kwargs.get('remove_excess_whitespace', self.default_remove_excess_whitespace),
            remove_urls=kwargs.get('remove_urls', self.default_remove_urls),
            min_line_length=kwargs.get('min_line_length', self.default_min_line_length),
            max_line_length=kwargs.get('max_line_length', self.default_max_line_length),
            extract_metadata=kwargs.get('extract_metadata', self.default_extract_metadata)
        )

    def set_default_extraction_method(self, method: str) -> None:
        self.default_extraction_method = method

    def set_default_remove_html(self, remove: bool) -> None:
        self.default_remove_html = remove

    def set_default_remove_excess_whitespace(self, remove: bool) -> None:
        self.default_remove_excess_whitespace = remove

    def set_default_remove_urls(self, remove: bool) -> None:
        self.default_remove_urls = remove

    def set_default_min_line_length(self, length: int) -> None:
        self.default_min_line_length = length

    def set_default_max_line_length(self, length: Optional[int]) -> None:
        self.default_max_line_length = length

    def set_default_extract_metadata(self, extract: bool) -> None:
        self.default_extract_metadata = extract
from spindle.abstracts import AbstractFetcherFactory
from spindle.fetchers import YouTubeFetcher
from spindle.processors import YouTubeProcessor
from spindle.services import YouTubeService
from spindle.handlers import FileHandler, ConsoleHandler
from spindle.config import ConfigManager
from spindle.factories import SerializerFactory

__all__ = ['YouTubeFetcherFactory']


class YouTubeFetcherFactory(AbstractFetcherFactory):
    def __init__(self):
        self.config = ConfigManager().get_config()
        self.youtube_service = YouTubeService(self.config.get('YOUTUBE_API_KEY'))
        self.serializer_factory = SerializerFactory()

    def _create_fetcher(self, **kwargs):
        processor = self._create_processor(**kwargs)
        return YouTubeFetcher(processor)

    def _create_processor(self, **kwargs):
        return YouTubeProcessor(self.youtube_service)

    def _create_handler(self, output=None, format='json', **kwargs):
        serializer = self.serializer_factory.create_serializer(format)
        if output:
            return FileHandler(serializer, output)
        else:
            return ConsoleHandler(serializer)

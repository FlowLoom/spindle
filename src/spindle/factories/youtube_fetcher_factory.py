from spindle.abstracts import AbstractFetcherFactory
from spindle.fetchers import YouTubeFetcher
from spindle.processors import YouTubeProcessor
from spindle.services import YouTubeService
from spindle.handlers import FileHandler, ConsoleHandler
from spindle.config import ConfigManager

__all__ = ['YouTubeFetcherFactory']


class YouTubeFetcherFactory(AbstractFetcherFactory):
    def __init__(self):
        self.config = ConfigManager().get_config()
        self.youtube_service = YouTubeService(self.config.get('YOUTUBE_API_KEY'))

    def _create_fetcher(self, **kwargs):
        processor = self._create_processor(**kwargs)
        return YouTubeFetcher(processor)

    def _create_processor(self, **kwargs):
        return YouTubeProcessor(self.youtube_service)

    def _create_handler(self, output=None, format='json', **kwargs):
        if output:
            return FileHandler(self._create_serializer(format), output)
        else:
            return ConsoleHandler(self._create_serializer(format))

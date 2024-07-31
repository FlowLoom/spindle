from spindle.abstracts import AbstractFetcherFactory
from spindle.fetchers import STDINFetcher
from spindle.processors import SaveProcessor
from spindle.handlers import SaveHandler
from spindle.config import ConfigManager

__All__ = ["SaveFetcherFactory"]


class SaveFetcherFactory(AbstractFetcherFactory):
    def __init__(self):
        self.config = ConfigManager().get_config()

    def _create_fetcher(self, **kwargs):
        processor = self._create_processor(**kwargs)
        return STDINFetcher(processor)

    def _create_processor(self, **kwargs):
        return SaveProcessor(self.config)

    def _create_handler(self, silent=False, passthrough=False, **kwargs):
        return SaveHandler(self.config, silent, passthrough)

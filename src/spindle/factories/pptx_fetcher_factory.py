from spindle.abstracts import AbstractFetcherFactory
from spindle.fetchers import PPTXFetcher
from spindle.processors import PPTXProcessor
from spindle.handlers import PPTXHandler

__all__ = ['PPTXFetcherFactory']


class PPTXFetcherFactory(AbstractFetcherFactory):
    def _create_fetcher(self, **kwargs):
        processor = self._create_processor(**kwargs)
        return PPTXFetcher(processor)

    def _create_processor(self, **kwargs):
        return PPTXProcessor()

    def _create_handler(self, output_file=None, **kwargs):
        return PPTXHandler(output_file)

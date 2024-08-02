# src/spindle/factories/pptx_setter_fetcher_factory.py

from spindle.abstracts import AbstractFetcherFactory
from spindle.fetchers import PPTXSetterFetcher
from spindle.processors import PPTXSetterProcessor
from spindle.handlers import PPTXSetterHandler

__all__ = ['PPTXSetterFetcherFactory']


class PPTXSetterFetcherFactory(AbstractFetcherFactory):
    def _create_fetcher(self, **kwargs):
        processor = self._create_processor(**kwargs)
        return PPTXSetterFetcher(processor)

    def _create_processor(self, **kwargs):
        return PPTXSetterProcessor()

    def _create_handler(self, output_file, **kwargs):
        return PPTXSetterHandler(output_file)

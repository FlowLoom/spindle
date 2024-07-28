from typing import Any, Type, List
from spindle.interfaces import ICerebro, IFetcher, IHandler, IProcessor

__All__ = ["AbstractCerebro"]


class AbstractCerebro(ICerebro):
    def __init__(self):
        self.fetchers = []
        self.processors = []
        self.handlers = []

    def add_processor(self, processor: Type[IProcessor]) -> None:
        self.processors.append(processor)

    def add_fetcher(self, fetcher: Type[IFetcher]) -> None:
        self.fetchers.append(fetcher)

    def add_handler(self, handler: Type[IHandler]) -> None:
        self.handlers.append(handler)

    def run(self, source: Any, *args, **kwargs) -> None:
        processed_data = {}

        # Run all parsers
        for fetcher_cls in self.fetchers:
            for processor_cls in self.processors:
                fetcher = fetcher_cls(processor_cls(), *args, **kwargs)
                processed_data.update(fetcher.parse(source))

        # Run all handlers
        for handler_cls in self.handlers:
            handler = handler_cls()
            handler.handle(processed_data)

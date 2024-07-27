from typing import Any, Type, List
from ct.interfaces import ICerebro, IParser, IHandler, IProcessor

__All__ = ["AbstractCerebro"]


class AbstractCerebro(ICerebro):
    def __init__(self):
        self.parsers = []
        self.processors = []
        self.handlers = []

    def add_processor(self, processor: Type[IProcessor]) -> None:
        self.processors.append(processor)

    def add_parser(self, parser: Type[IParser]) -> None:
        self.parsers.append(parser)

    def add_handler(self, handler: Type[IHandler]) -> None:
        self.handlers.append(handler)

    def run(self, source: Any, *args, **kwargs) -> None:
        processed_data = {}

        # Run all parsers
        for parser_cls in self.parsers:
            for processor_cls in self.processors:
                parser = parser_cls(processor_cls(), *args, **kwargs)
                processed_data.update(parser.parse(source))

        # Run all handlers
        for handler_cls in self.handlers:
            handler = handler_cls()
            handler.handle(processed_data)

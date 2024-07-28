from spindle.interfaces import IFetcher
from typing import Dict, List

__All__ = ["AbstractFetcherDecorator"]


class AbstractFetcherDecorator(IFetcher):
    def __init__(self, wrapped_fetcher: IFetcher):
        self.wrapped_fetcher = wrapped_fetcher

    def fetch(self) -> Dict[str, List[str]]:
        return self.wrapped_parser.fetch()

    def accept(self, visitor):
        self.wrapped_parser.accept(visitor)
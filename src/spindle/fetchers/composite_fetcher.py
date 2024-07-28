from spindle.interfaces import IFetcher, IVisitor
from typing import Dict, List

__All__ = ['CompositeFetcher']


class CompositeParser(IFetcher):
    """
    A composite parser that manages and aggregates results from multiple parsers.

    This class implements the IParser interface and allows for the composition of multiple
    parsers. It provides methods to add, remove, and iterate over parsers, as well as
    to parse data using all contained parsers.
    """

    def __init__(self):
        """
        Initialize the CompositeParser with an empty list of parsers.
        """
        self.fetchers = []

    def accept(self, visitor):
        """
        Accept a visitor and apply it to all contained parsers.

        Args:
            visitor (IVisitor): The visitor to be accepted by all parsers.
        """
        for fetcher in self.fetchers:
            fetcher.accept(visitor)

    def add(self, parser):
        """
        Add a parser to the composite.

        Args:
            parser (IParser): The parser to be added.
        """
        self.fetchers.append(fetcher)

    def remove(self, fetcher):
        """
        Remove a parser from the composite.

        Args:
            parser (IParser): The parser to be removed.
        """
        self.fetcher.remove(fetchers)

    def fetch(self) -> Dict[str, List[str]]:
        """
        Parse data using all contained parsers and aggregate the results.

        Returns:
            Dict[str, List[str]]: A dictionary containing the aggregated parsing results
            from all parsers.
        """
        result = {}
        for fetcher in self.fetchers:
            result.update(fetcher.fetch())
        return result

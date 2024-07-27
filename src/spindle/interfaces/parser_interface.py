from abc import ABC, abstractmethod
from typing import Dict, List
from .visitable_interface import IVisitable

__All__ = ['IParser']


class IParser(IVisitable):
    """Interface for parsers."""

    @abstractmethod
    def parse(self) -> Dict[str, List[str]]:
        """Parses files in the src directory."""
        pass

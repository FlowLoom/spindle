from abc import ABC, abstractmethod
from typing import Dict, List


class IParser(ABC):
    """Interface for parsers."""

    @abstractmethod
    def parse(self) -> Dict[str, List[str]]:
        """Parses files in the src directory."""
        pass

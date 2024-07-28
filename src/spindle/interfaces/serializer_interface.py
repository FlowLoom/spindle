from abc import ABC, abstractmethod
from typing import Dict, Any

__All__ = ["ISerializer"]


class ISerializer(ABC):
    @abstractmethod
    def encode(self, data: Dict[str, Any]) -> str:
        """Serialize the data to a string."""
        pass

    @abstractmethod
    def decode(self, data: str) -> Dict[str, Any]:
        """Deserialize the string to a dictionary."""
        pass
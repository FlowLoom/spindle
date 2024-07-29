from abc import ABC, abstractmethod
from typing import List, Dict, Any, Generator

__All__ = ['IModelProvider']


class IModelProvider(ABC):
    @abstractmethod
    def get_models(self) -> List[str]:
        """Fetch and return a list of available models from the AI service."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if the AI service is available and properly configured."""
        pass

    @abstractmethod
    def get_default_model(self) -> str:
        """Get the default model for the AI service."""
        pass

    @abstractmethod
    def validate_model(self, model_name: str) -> bool:
        """Validate if a given model name is available in the AI service."""
        pass

    @abstractmethod
    def send_message(self, messages: List[Dict[str, str]], model: str, args: Dict[str, Any]) -> str:
        """Send a message to the AI service and return the response."""
        pass

    @abstractmethod
    def stream_message(self, messages: List[Dict[str, str]], model: str, args: Dict[str, Any]) -> Generator[
        str, None, None]:
        """Stream a message to the AI service and yield the response chunks."""
        pass

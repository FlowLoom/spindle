from typing import Dict, Type, Optional, List
from spindle.interfaces.model_provider_interface import IModelProvider
from spindle.providers.gpt_model_provider import GPTModelProvider
from spindle.providers import ClaudeModelProvider
from spindle.providers import GoogleModelProvider
from spindle.providers import OllamaModelProvider

__all__ = ["ModelProviderFactory"]


class ModelProviderFactory:
    """
    Factory class for creating ModelProvider instances.
    """

    def __init__(self):
        self._providers: Dict[str, Type[IModelProvider]] = {
            "gpt": GPTModelProvider,
            "claude": ClaudeModelProvider,
            "google": GoogleModelProvider,
            "ollama": OllamaModelProvider
        }

    def create_provider(self, provider_type: str, **kwargs) -> Optional[IModelProvider]:
        """
        Create and return an instance of the specified ModelProvider.

        Args:
            provider_type (str): The type of ModelProvider to create.
            **kwargs: Additional keyword arguments to pass to the ModelProvider constructor.

        Returns:
            Optional[IModelProvider]: An instance of the specified ModelProvider, or None if the type is not recognized.
        """
        provider_class = self._providers.get(provider_type.lower())
        if provider_class:
            return provider_class(**kwargs)
        else:
            print(f"Unsupported provider type: {provider_type}")
            return None

    def register_provider(self, provider_type: str, provider_class: Type[IModelProvider]) -> None:
        """
        Register a new ModelProvider type.

        Args:
            provider_type (str): The type name for the new ModelProvider.
            provider_class (Type[IModelProvider]): The class of the new ModelProvider.
        """
        self._providers[provider_type.lower()] = provider_class

    def get_available_providers(self) -> List[str]:
        """
        Get a list of all available ModelProvider types.

        Returns:
            List[str]: A list of available ModelProvider type names.
        """
        return list(self._providers.keys())
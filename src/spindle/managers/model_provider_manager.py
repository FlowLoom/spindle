from typing import Dict, Optional, List
from spindle.factories import ModelProviderFactory
from spindle.interfaces import IModelProvider

__All__ = ["ModelProviderManager"]


class ModelProviderManager:
    def __init__(self):
        self.model_provider_factory = ModelProviderFactory()

    def get_model_provider(self, provider_type: str, **kwargs) -> Optional[IModelProvider]:
        """
        Get a ModelProvider instance for the specified type.

        Args:
            provider_type (str): The type of ModelProvider to get.
            **kwargs: Additional keyword arguments to pass to the ModelProvider constructor.

        Returns:
            Optional[IModelProvider]: An instance of the specified ModelProvider, or None if the type is not recognized.
        """
        return self.model_provider_factory.create_provider(provider_type, **kwargs)

    def get_available_model_providers(self) -> List[str]:
        """
        Get a list of all available ModelProvider types.

        Returns:
            List[str]: A list of available ModelProvider type names.
        """
        return self.model_provider_factory.get_available_providers()

    def initialize_model_providers(self) -> Dict[str, List[str]]:
        """
        Initialize all model providers and return a dictionary of available models for each provider.
        """
        available_models = {}
        for provider_type in self.get_available_model_providers():
            provider = self.get_model_provider(provider_type)
            if provider and provider.is_available():
                available_models[provider_type] = provider.get_models()
        return available_models

    def validate_model(self, provider_type: str, model_name: str) -> bool:
        """
        Validate if a given model is available for a specific provider.

        Args:
            provider_type (str): The type of ModelProvider to use.
            model_name (str): The name of the model to validate.

        Returns:
            bool: True if the model is valid and available, False otherwise.
        """
        provider = self.get_model_provider(provider_type)
        if provider and provider.is_available():
            return provider.validate_model(model_name)
        return False

    def get_default_model(self, provider_type: str) -> Optional[str]:
        """
        Get the default model for a specific provider.

        Args:
            provider_type (str): The type of ModelProvider to use.

        Returns:
            Optional[str]: The name of the default model, or None if not available.
        """
        provider = self.get_model_provider(provider_type)
        if provider and provider.is_available():
            return provider.get_default_model()
        return None

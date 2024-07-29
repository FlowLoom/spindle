# src/spindle/config/config_manager.py

import os
from typing import Any, Optional, Dict
from dotenv import load_dotenv
from spindle.interfaces import IConfigurationManager, IModelProvider
from spindle.factories import ModelProviderFactory

__All__ = ["ConfigManager"]


class ConfigManager(IConfigurationManager):
    def __init__(self):
        self.config_dir = os.path.expanduser("~/.config/spindle")
        self.env_file = os.path.join(self.config_dir, ".env")
        self.config: Dict[str, Any] = {}
        self.model_provider_factory = ModelProviderFactory()
        self._ensure_config_dir()
        self.load()

    def _ensure_config_dir(self):
        """Ensure the configuration directory exists."""
        os.makedirs(self.config_dir, exist_ok=True)

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Retrieve a configuration value."""
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        self.config[key] = value
        self.save()

    def load(self) -> None:
        """Load configuration from the .env file."""
        if os.path.exists(self.env_file):
            load_dotenv(self.env_file)
        self.config = dict(os.environ)

    def save(self) -> None:
        """Save the current configuration to the .env file."""
        with open(self.env_file, "w") as f:
            for key, value in self.config.items():
                f.write(f"{key}={value}\n")

    def get_config_dir(self) -> str:
        """Get the configuration directory path."""
        return self.config_dir

    def get_patterns_dir(self) -> str:
        """Get the patterns directory path."""
        return os.path.join(self.config_dir, "patterns")

    def get_all(self) -> Dict[str, Any]:
        """Get all configuration key-value pairs."""
        return self.config.copy()

    def clear(self) -> None:
        """Clear all configuration settings."""
        self.config.clear()
        self.save()

    def exists(self, key: str) -> bool:
        """Check if a configuration key exists."""
        return key in self.config

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

    def get_available_model_providers(self):
        """
        Get a list of all available ModelProvider types.

        Returns:
            List[str]: A list of available ModelProvider type names.
        """
        return self.model_provider_factory.get_available_providers()

    def initialize_model_providers(self):
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

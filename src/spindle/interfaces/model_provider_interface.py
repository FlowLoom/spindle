from abc import ABC, abstractmethod
from typing import List

__All__ = ["IModelProvider"]


class IModelProvider(ABC):
    """
    Interface for model providers that fetch available models from different AI services.
    """

    @abstractmethod
    def get_models(self) -> List[str]:
        """
        Fetch and return a list of available models from the AI service.

        Returns:
            List[str]: A list of model names available from the service.
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the AI service is available and properly configured.

        Returns:
            bool: True if the service is available, False otherwise.
        """
        pass

    @abstractmethod
    def get_default_model(self) -> str:
        """
        Get the default model for the AI service.

        Returns:
            str: The name of the default model.
        """
        pass

    @abstractmethod
    def validate_model(self, model_name: str) -> bool:
        """
        Validate if a given model name is available in the AI service.

        Args:
            model_name (str): The name of the model to validate.

        Returns:
            bool: True if the model is valid and available, False otherwise.
        """
        pass
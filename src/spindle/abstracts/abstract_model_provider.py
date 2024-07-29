import logging
from abc import abstractmethod
from typing import List, Optional
from spindle.interfaces.model_provider_interface import IModelProvider

__All__ = ["AbstractModelProvider"]


class AbstractModelProvider(IModelProvider):
    """
    Abstract base class for model providers, implementing common functionality
    and error handling for all concrete model provider classes.
    """

    def __init__(self, service_name: str):
        self.service_name = service_name
        self.logger = logging.getLogger(f"{self.__class__.__name__}")

    def get_models(self) -> List[str]:
        """
        Fetch and return a list of available models from the AI service.
        Implements error handling and logging.

        Returns:
            List[str]: A list of model names available from the service.
        """
        try:
            models = self._fetch_models()
            self.logger.info(f"Successfully fetched {len(models)} models from {self.service_name}")
            return models
        except Exception as e:
            self.logger.error(f"Error fetching models from {self.service_name}: {str(e)}")
            return []

    @abstractmethod
    def _fetch_models(self) -> List[str]:
        """
        Abstract method to be implemented by concrete classes for fetching models.

        Returns:
            List[str]: A list of model names available from the service.
        """
        pass

    def is_available(self) -> bool:
        """
        Check if the AI service is available and properly configured.

        Returns:
            bool: True if the service is available, False otherwise.
        """
        try:
            return self._check_availability()
        except Exception as e:
            self.logger.error(f"Error checking availability of {self.service_name}: {str(e)}")
            return False

    @abstractmethod
    def _check_availability(self) -> bool:
        """
        Abstract method to be implemented by concrete classes for checking service availability.

        Returns:
            bool: True if the service is available, False otherwise.
        """
        pass

    def get_default_model(self) -> Optional[str]:
        """
        Get the default model for the AI service.

        Returns:
            Optional[str]: The name of the default model, or None if not available.
        """
        try:
            default_model = self._get_default_model()
            if default_model:
                self.logger.info(f"Default model for {self.service_name}: {default_model}")
            else:
                self.logger.warning(f"No default model available for {self.service_name}")
            return default_model
        except Exception as e:
            self.logger.error(f"Error getting default model for {self.service_name}: {str(e)}")
            return None

    @abstractmethod
    def _get_default_model(self) -> Optional[str]:
        """
        Abstract method to be implemented by concrete classes for getting the default model.

        Returns:
            Optional[str]: The name of the default model, or None if not available.
        """
        pass

    def validate_model(self, model_name: str) -> bool:
        """
        Validate if a given model name is available in the AI service.

        Args:
            model_name (str): The name of the model to validate.

        Returns:
            bool: True if the model is valid and available, False otherwise.
        """
        try:
            is_valid = self._validate_model(model_name)
            if is_valid:
                self.logger.info(f"Model '{model_name}' is valid for {self.service_name}")
            else:
                self.logger.warning(f"Model '{model_name}' is not valid for {self.service_name}")
            return is_valid
        except Exception as e:
            self.logger.error(f"Error validating model '{model_name}' for {self.service_name}: {str(e)}")
            return False

    @abstractmethod
    def _validate_model(self, model_name: str) -> bool:
        """
        Abstract method to be implemented by concrete classes for validating a model.

        Args:
            model_name (str): The name of the model to validate.

        Returns:
            bool: True if the model is valid and available, False otherwise.
        """
        pass
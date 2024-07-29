import logging
from typing import List, Dict, Any, Generator, Optional
from abc import abstractmethod
from spindle.interfaces import IModelProvider

__All__ = ["AbstractModelProvider"]


class AbstractModelProvider(IModelProvider):
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.logger = logging.getLogger(f"{self.__class__.__name__}")

    def get_models(self) -> List[str]:
        try:
            models = self._fetch_models()
            self.logger.info(f"Successfully fetched {len(models)} models from {self.service_name}")
            return models
        except Exception as e:
            self.logger.error(f"Error fetching models from {self.service_name}: {str(e)}")
            return []

    def is_available(self) -> bool:
        try:
            return self._check_availability()
        except Exception as e:
            self.logger.error(f"Error checking availability of {self.service_name}: {str(e)}")
            return False

    def get_default_model(self) -> Optional[str]:
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

    def validate_model(self, model_name: str) -> bool:
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

    def send_message(self, messages: List[Dict[str, str]], model: str, args: Dict[str, Any]) -> str:
        try:
            response = self._send_message(messages, model, args)
            self.logger.info(f"Successfully sent message to {self.service_name} using model {model}")
            return response
        except Exception as e:
            self.logger.error(f"Error sending message to {self.service_name} using model {model}: {str(e)}")
            raise

    def stream_message(self, messages: List[Dict[str, str]], model: str, args: Dict[str, Any]) -> Generator[str, None, None]:
        try:
            for chunk in self._stream_message(messages, model, args):
                yield chunk
            self.logger.info(f"Successfully streamed message from {self.service_name} using model {model}")
        except Exception as e:
            self.logger.error(f"Error streaming message from {self.service_name} using model {model}: {str(e)}")
            raise

    @abstractmethod
    def _fetch_models(self) -> List[str]:
        pass

    @abstractmethod
    def _check_availability(self) -> bool:
        pass

    @abstractmethod
    def _get_default_model(self) -> Optional[str]:
        pass

    @abstractmethod
    def _validate_model(self, model_name: str) -> bool:
        pass

    @abstractmethod
    def _send_message(self, messages: List[Dict[str, str]], model: str, args: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def _stream_message(self, messages: List[Dict[str, str]], model: str, args: Dict[str, Any]) -> Generator[str, None, None]:
        pass

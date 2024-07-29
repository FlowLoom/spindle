from typing import List, Optional
from spindle.abstracts import AbstractModelProvider

__All__ = ["OllamaModelProvider"]


class OllamaModelProvider(AbstractModelProvider):
    def __init__(self, remote_server: Optional[str] = None):
        super().__init__("Ollama")
        self.remote_server = remote_server
        self.models = []
        self.initialize_client()

    def initialize_client(self):
        try:
            import ollama
            if self.remote_server:
                client = ollama.Client(host=self.remote_server)
                self.models = [model['name'] for model in client.list()['models']]
            else:
                self.models = [model['name'] for model in ollama.list()['models']]
        except ImportError:
            self.logger.warning("Ollama library is not installed.")
        except Exception as e:
            self.logger.error(f"Error initializing Ollama client: {str(e)}")

    def _fetch_models(self) -> List[str]:
        return self.models

    def _check_availability(self) -> bool:
        return bool(self.models)

    def _get_default_model(self) -> Optional[str]:
        return self.models[0] if self.models else None

    def _validate_model(self, model_name: str) -> bool:
        return model_name in self.models
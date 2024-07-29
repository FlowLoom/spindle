import os
from typing import List, Optional
from openai import OpenAI, APIConnectionError
from spindle.abstracts import AbstractModelProvider

__All__ = ["GPTModelProvider"]


class GPTModelProvider(AbstractModelProvider):
    def __init__(self):
        super().__init__("GPT")
        self.client = None
        self.initialize_client()

    def initialize_client(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            self.client = OpenAI(api_key=api_key)

    def _fetch_models(self) -> List[str]:
        if not self.client:
            return []

        models = [model.id.strip() for model in self.client.models.list().data]
        if "/" in models[0] or "\\" in models[0]:
            return [item[item.rfind("/") + 1:] if "/" in item else item[item.rfind("\\") + 1:] for item in models]
        else:
            return [item.strip() for item in models if item.startswith("gpt")]

    def _check_availability(self) -> bool:
        return bool(self.client)

    def _get_default_model(self) -> Optional[str]:
        models = self._fetch_models()
        return models[0] if models else None

    def _validate_model(self, model_name: str) -> bool:
        return model_name in self._fetch_models()
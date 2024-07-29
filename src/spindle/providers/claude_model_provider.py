import os
from typing import List, Optional
from spindle.abstracts import AbstractModelProvider

__All__ = ["ClaudeModelProvider"]

class ClaudeModelProvider(AbstractModelProvider):
    def __init__(self):
        super().__init__("Claude")
        self.models = [
            'claude-3-5-sonnet-20240620',
            'claude-3-opus-20240229',
            'claude-3-sonnet-20240229',
            'claude-3-haiku-20240307',
            'claude-2.1'
        ]

    def _fetch_models(self) -> List[str]:
        return self.models if self._check_availability() else []

    def _check_availability(self) -> bool:
        return bool(os.getenv("CLAUDE_API_KEY"))

    def _get_default_model(self) -> Optional[str]:
        return self.models[0] if self.models else None

    def _validate_model(self, model_name: str) -> bool:
        return model_name in self.models
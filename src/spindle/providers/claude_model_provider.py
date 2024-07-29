from typing import List, Dict, Any, Generator, Optional
from anthropic import Anthropic
from spindle.abstracts import AbstractModelProvider

__all__ = ["ClaudeModelProvider"]


class ClaudeModelProvider(AbstractModelProvider):
    def __init__(self, api_key: str):
        super().__init__("Claude")
        self.client = Anthropic(api_key=api_key)
        self.models = [
            'claude-3-5-sonnet-20240620',
            'claude-3-opus-20240229',
            'claude-3-sonnet-20240229',
            'claude-3-haiku-20240307',
            'claude-2.1'
        ]

    def _fetch_models(self) -> List[str]:
        return self.models

    def _check_availability(self) -> bool:
        return bool(self.client)

    def _get_default_model(self) -> Optional[str]:
        return self.models[0] if self.models else None

    def _validate_model(self, model_name: str) -> bool:
        return model_name in self.models

    def _send_message(self, messages: List[Dict[str, str]], model: str, args: Dict[str, Any]) -> str:
        response = self.client.messages.create(
            model=model,
            max_tokens=args.get('max_tokens', 1000),
            messages=messages,
            temperature=args.get('temp', 0),
            top_p=args.get('top_p', 1),
        )
        return response.content[0].text

    def _stream_message(self, messages: List[Dict[str, str]], model: str, args: Dict[str, Any]) -> Generator[str, None, None]:
        stream = self.client.messages.create(
            model=model,
            max_tokens=args.get('max_tokens', 1000),
            messages=messages,
            temperature=args.get('temp', 0),
            top_p=args.get('top_p', 1),
            stream=True,
        )
        for chunk in stream:
            if chunk.delta.text:
                yield chunk.delta.text

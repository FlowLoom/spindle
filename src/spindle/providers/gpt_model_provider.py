from typing import List, Dict, Any, Generator, Optional
from openai import OpenAI
from spindle.abstracts import AbstractModelProvider

__all__ = ["GPTModelProvider"]


class GPTModelProvider(AbstractModelProvider):
    def __init__(self, api_key: str):
        super().__init__("GPT")
        self.client = OpenAI(api_key=api_key)

    def _fetch_models(self) -> List[str]:
        models = [model.id.strip() for model in self.client.models.list().data]
        return [item.strip() for item in models if item.startswith("gpt")]

    def _check_availability(self) -> bool:
        return bool(self.client)

    def _get_default_model(self) -> Optional[str]:
        models = self._fetch_models()
        return models[0] if models else None

    def _validate_model(self, model_name: str) -> bool:
        return model_name in self._fetch_models()

    def _send_message(self, messages: List[Dict[str, str]], model: str, args: Dict[str, Any]) -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=args.get('temp', 0),
            top_p=args.get('top_p', 1),
            frequency_penalty=args.get('frequency_penalty', 0.1),
            presence_penalty=args.get('presence_penalty', 0.1),
        )
        return response.choices[0].message.content

    def _stream_message(self, messages: List[Dict[str, str]], model: str, args: Dict[str, Any]) -> Generator[str, None, None]:
        stream = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=args.get('temp', 0),
            top_p=args.get('top_p', 1),
            frequency_penalty=args.get('frequency_penalty', 0.1),
            presence_penalty=args.get('presence_penalty', 0.1),
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

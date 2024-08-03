from typing import Dict, List, Generator
from openai import OpenAI
from spindle.config import ConfigManager
from spindle.exceptions import SpindleException

__all__ = ['UnifyService']


class UnifyService:
    def __init__(self, config: ConfigManager):
        self.config = config
        self.unify_key = config.get('UNIFY_KEY')
        self.openai_key = config.get('OPENAI_API_KEY')
        self.unify_client = OpenAI(api_key=self.unify_key, base_url="https://api.unify.ai/v0/")
        self.openai_client = OpenAI(api_key=self.openai_key)

    def send_message(self, messages: List[Dict[str, str]], args: Dict) -> str:
        try:
            client = self._get_client(args.get('model'))
            response = client.chat.completions.create(
                model=args.get('model', self.config.get('DEFAULT_MODEL')),
                messages=messages,
                temperature=args.get('temp', 0),
                max_tokens=args.get('max_tokens', 4096),
                top_p=args.get('top_p', 1),
            )
            return response.choices[0].message.content
        except Exception as e:
            raise SpindleException(f"Unify API error: {str(e)}")

    def stream_message(self, messages: List[Dict[str, str]], args: Dict) -> Generator[str, None, None]:
        try:
            client = self._get_client(args.get('model'))
            stream = client.chat.completions.create(
                model=args.get('model', self.config.get('DEFAULT_MODEL')),
                messages=messages,
                temperature=args.get('temp', 0),
                max_tokens=args.get('max_tokens', 4096),
                top_p=args.get('top_p', 1),
                stream=True,
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            raise SpindleException(f"Unify API streaming error: {str(e)}")

    def _get_client(self, model: str):
        return self.openai_client if "embedding" in model else self.unify_client

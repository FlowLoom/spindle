from typing import Dict, List, Generator
from mistralai.client import MistralClient
from spindle.config import ConfigManager
from spindle.exceptions import SpindleException

__all__ = ['MistralService']


class MistralService:
    def __init__(self, config: ConfigManager):
        self.config = config
        self.client = MistralClient(api_key=config.get('MISTRAL_API_KEY'))

    def send_message(self, messages: List[Dict[str, str]], args: Dict) -> str:
        try:
            response = self.client.chat(
                model=args.get('model', self.config.get('DEFAULT_MODEL')),
                messages=messages,
                temperature=args.get('temp', 0),
                top_p=args.get('top_p', 1),
                max_tokens=args.get('max_tokens', 4096),
            )
            return response.choices[0].message.content
        except Exception as e:
            raise SpindleException(f"Mistral API error: {str(e)}")

    def stream_message(self, messages: List[Dict[str, str]], args: Dict) -> Generator[str, None, None]:
        try:
            stream = self.client.chat_stream(
                model=args.get('model', self.config.get('DEFAULT_MODEL')),
                messages=messages,
                temperature=args.get('temp', 0),
                top_p=args.get('top_p', 1),
                max_tokens=args.get('max_tokens', 4096),
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            raise SpindleException(f"Mistral API streaming error: {str(e)}")

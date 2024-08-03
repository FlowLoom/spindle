from typing import Dict, List, Generator
from huggingface_hub import InferenceClient
from spindle.config import ConfigManager
from spindle.exceptions import SpindleException

__all__ = ['HuggingFaceService']


class HuggingFaceService:
    def __init__(self, config: ConfigManager):
        self.config = config
        self.client = InferenceClient(token=config.get('HUGGINGFACE_API_KEY'))

    def send_message(self, messages: List[Dict[str, str]], args: Dict) -> str:
        try:
            response = self.client.text_generation(
                model=args.get('model', self.config.get('DEFAULT_MODEL')),
                prompt=self._format_messages(messages),
                max_new_tokens=args.get('max_tokens', 4096),
                temperature=args.get('temp', 0),
                top_p=args.get('top_p', 1),
            )
            return response[0]['generated_text']
        except Exception as e:
            raise SpindleException(f"HuggingFace API error: {str(e)}")

    def stream_message(self, messages: List[Dict[str, str]], args: Dict) -> Generator[str, None, None]:
        try:
            stream = self.client.text_generation(
                model=args.get('model', self.config.get('DEFAULT_MODEL')),
                prompt=self._format_messages(messages),
                max_new_tokens=args.get('max_tokens', 4096),
                temperature=args.get('temp', 0),
                top_p=args.get('top_p', 1),
                stream=True,
            )
            for response in stream:
                if response.token.text:
                    yield response.token.text
        except Exception as e:
            raise SpindleException(f"HuggingFace API streaming error: {str(e)}")

    def _format_messages(self, messages: List[Dict[str, str]]) -> str:
        formatted = ""
        for message in messages:
            if message['role'] == 'system':
                formatted += f"System: {message['content']}\n"
            elif message['role'] == 'user':
                formatted += f"Human: {message['content']}\n"
            elif message['role'] == 'assistant':
                formatted += f"Assistant: {message['content']}\n"
        return formatted.strip()

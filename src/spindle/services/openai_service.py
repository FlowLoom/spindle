from typing import Dict, List, Generator
from openai import OpenAI
from spindle.config import ConfigManager
from spindle.exceptions import SpindleException

__All__ = ['OpenAIService']


class OpenAIService:
    def __init__(self, config: ConfigManager):
        self.config = config
        self.client = OpenAI(api_key=config.get('OPENAI_API_KEY'))

    def send_message(self, messages: List[Dict[str, str]], args: Dict) -> str:
        try:
            response = self.client.chat.completions.create(
                model=args.get('model', self.config.get('DEFAULT_MODEL')),
                messages=messages,
                temperature=args.get('temp', 0),
                top_p=args.get('top_p', 1),
                frequency_penalty=args.get('frequency_penalty', 0.1),
                presence_penalty=args.get('presence_penalty', 0.1),
            )
            return response.choices[0].message.content
        except Exception as e:
            raise SpindleException(f"OpenAI API error: {str(e)}")

    def stream_message(self, messages: List[Dict[str, str]], args: Dict) -> Generator[str, None, None]:
        try:
            stream = self.client.chat.completions.create(
                model=args.get('model', self.config.get('DEFAULT_MODEL')),
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
        except Exception as e:
            raise SpindleException(f"OpenAI API streaming error: {str(e)}")
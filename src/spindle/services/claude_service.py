from typing import Dict, List, Generator
from anthropic import Anthropic
from spindle.config import ConfigManager
from spindle.exceptions import SpindleException

__All__ = ['ClaudeService']


class ClaudeService:
    def __init__(self, config: ConfigManager):
        self.config = config
        self.client = Anthropic(api_key=config.get('CLAUDE_API_KEY'))

    def send_message(self, messages: List[Dict[str, str]], args: Dict) -> str:
        try:
            response = self.client.messages.create(
                model=args.get('model', self.config.get('DEFAULT_MODEL')),
                max_tokens=4096,
                messages=messages,
                temperature=args.get('temp', 0),
                top_p=args.get('top_p', 1),
            )
            return response.content[0].text
        except Exception as e:
            raise SpindleException(f"Claude API error: {str(e)}")

    def stream_message(self, messages: List[Dict[str, str]], args: Dict) -> Generator[str, None, None]:
        try:
            stream = self.client.messages.create(
                model=args.get('model', self.config.get('DEFAULT_MODEL')),
                max_tokens=4096,
                messages=messages,
                temperature=args.get('temp', 0),
                top_p=args.get('top_p', 1),
                stream=True,
            )
            for chunk in stream:
                if chunk.delta.text:
                    yield chunk.delta.text
        except Exception as e:
            raise SpindleException(f"Claude API streaming error: {str(e)}")
from typing import Dict, List, Generator
import google.generativeai as genai
from spindle.config import ConfigManager
from spindle.exceptions import SpindleException

__All__ = ['GoogleService']


class GoogleService:
    def __init__(self, config: ConfigManager):
        self.config = config
        genai.configure(api_key=config.get('GOOGLE_API_KEY'))

    def send_message(self, messages: List[Dict[str, str]], args: Dict) -> str:
        try:
            model = genai.GenerativeModel(model_name=args.get('model', self.config.get('DEFAULT_MODEL')))
            response = model.generate_content(messages[-1]['content'])  # Assuming last message is user's input
            return response.text
        except Exception as e:
            raise SpindleException(f"Google AI error: {str(e)}")

    def stream_message(self, messages: List[Dict[str, str]], args: Dict) -> Generator[str, None, None]:
        try:
            model = genai.GenerativeModel(model_name=args.get('model', self.config.get('DEFAULT_MODEL')))
            response = model.generate_content(messages[-1]['content'], stream=True)
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            raise SpindleException(f"Google AI streaming error: {str(e)}")
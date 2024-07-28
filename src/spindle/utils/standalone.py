import os
from typing import Any, Dict, List
from spindle.config import ConfigManager
from spindle.services import OpenAIService, ClaudeService, GoogleService, OllamaService
from spindle.exceptions import SpindleException

class Standalone:
    def __init__(self, args: Dict[str, Any], pattern: str = ""):
        self.config = ConfigManager()
        self.args = args
        self.pattern = pattern
        self.model = self._get_model()
        self.service = self._initialize_service()

    def _get_model(self) -> str:
        return self.args.get('model') or self.config.get('DEFAULT_MODEL', 'gpt-4-turbo-preview')

    def _initialize_service(self):
        if self.model in self.config.get_gpt_models():
            return OpenAIService(self.config)
        elif self.model in self.config.get_claude_models():
            return ClaudeService(self.config)
        elif self.model in self.config.get_google_models():
            return GoogleService(self.config)
        elif self.model in self.config.get_ollama_models():
            return OllamaService(self.config)
        else:
            raise SpindleException(f"Unsupported model: {self.model}")

    def send_message(self, input_data: str, context: str = "", host: str = ''):
        system_message = self._get_system_message(context)
        user_message = {"role": "user", "content": input_data}
        messages = [system_message, user_message] if system_message else [user_message]

        response = self.service.send_message(messages, self.args)
        self._handle_output(response)

    def stream_message(self, input_data: str, context: str = "", host: str = ''):
        system_message = self._get_system_message(context)
        user_message = {"role": "user", "content": input_data}
        messages = [system_message, user_message] if system_message else [user_message]

        for chunk in self.service.stream_message(messages, self.args):
            print(chunk, end='', flush=True)

    def _get_system_message(self, context: str) -> Dict[str, str]:
        if not self.pattern:
            return {"role": "system", "content": context} if context else {}

        pattern_file = os.path.join(self.config.get_patterns_dir(), f"{self.pattern}/system.md")
        try:
            with open(pattern_file, "r") as f:
                content = f.read()
                if context:
                    content = f"{context}\n\n{content}"
                return {"role": "system", "content": content}
        except FileNotFoundError:
            raise SpindleException(f"Pattern file not found: {pattern_file}")

    def _handle_output(self, response: str):
        if self.args.get('copy'):
            import pyperclip
            pyperclip.copy(response)

        if output_file := self.args.get('output'):
            with open(output_file, "w") as f:
                f.write(response)

        print(response)

    @staticmethod
    def get_cli_input() -> str:
        return input("Enter your message: ")
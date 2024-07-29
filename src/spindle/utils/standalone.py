from typing import Dict, Any
from spindle.config import ConfigManager
from spindle.exceptions import SpindleException

__All__ = ['Standalone']


class Standalone:
    def __init__(self, args: Dict[str, Any], pattern: str = ""):
        self.config_manager = ConfigManager()
        self.args = args
        self.pattern = pattern
        self.model = self._get_model()
        self.service = self._initialize_service()

    def _get_model(self) -> str:
        config = self.config_manager.get_config()
        return self.args.get('model') or config.get('DEFAULT_MODEL', 'gpt-4-turbo-preview')

    def _initialize_service(self):
        model_provider_manager = self.config_manager.get_model_provider_manager()

        if self.model.startswith('gpt'):
            provider = model_provider_manager.get_model_provider('gpt')
        elif self.model.startswith('claude'):
            provider = model_provider_manager.get_model_provider('claude')
        elif self.model.startswith('gemini'):
            provider = model_provider_manager.get_model_provider('google')
        elif model_provider_manager.get_model_provider('ollama').validate_model(self.model):
            provider = model_provider_manager.get_model_provider('ollama')
        else:
            raise SpindleException(f"Unsupported model: {self.model}")

        if not provider:
            raise SpindleException(f"Failed to initialize provider for model: {self.model}")

        return provider

    def send_message(self, input_data: str, context: str = "", host: str = ''):
        system_message = self._get_system_message(context)
        user_message = {"role": "user", "content": input_data}
        messages = [system_message, user_message] if system_message else [user_message]

        response = self.service.send_message(messages, self.model, self.args)
        self._handle_output(response)

    def stream_message(self, input_data: str, context: str = "", host: str = ''):
        system_message = self._get_system_message(context)
        user_message = {"role": "user", "content": input_data}
        messages = [system_message, user_message] if system_message else [user_message]

        for chunk in self.service.stream_message(messages, self.model, self.args):
            print(chunk, end='', flush=True)

    def _get_system_message(self, context: str) -> Dict[str, str]:
        config = self.config_manager.get_config()
        if not self.pattern:
            return {"role": "system", "content": context} if context else {}

        pattern_file = os.path.join(config.get_patterns_dir(), f"{self.pattern}/system.md")
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

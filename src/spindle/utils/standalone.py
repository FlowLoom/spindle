import os
from typing import Dict, List, Any, Optional
from spindle.config.config_manager import ConfigManager
from spindle.exceptions import SpindleException
from spindle.interfaces import IModelProvider

__All__ = ["Standalone"]


class Standalone:
    def __init__(self, args: Dict[str, Any], pattern: str = ""):
        self.config_manager = ConfigManager()
        self.args = args
        self.pattern = pattern
        self.model = self._get_model()
        self.provider = self._initialize_provider()

    def _get_model(self) -> str:
        config = self.config_manager.get_config()
        return self.args.get('model') or config.get('DEFAULT_MODEL', 'gpt-4-turbo-preview')

    def _initialize_provider(self) -> Optional[IModelProvider]:
        model_provider_manager = self.config_manager.get_model_provider_manager()
        config = self.config_manager.get_config()

        provider_type = self._get_provider_type()
        provider_args = self._get_provider_args(provider_type, config)

        provider = model_provider_manager.get_model_provider(provider_type, **provider_args)

        if not provider:
            raise SpindleException(f"Failed to initialize provider for model: {self.model}")

        if not provider.validate_model(self.model):
            raise SpindleException(f"Invalid model {self.model} for provider {provider_type}")

        return provider

    def _get_provider_type(self) -> str:
        if self.model.startswith('gpt'):
            return 'gpt'
        elif self.model.startswith('claude'):
            return 'claude'
        elif self.model.startswith('gemini'):
            return 'google'
        else:
            return 'ollama'  # Default to Ollama for unknown models

    def _get_provider_args(self, provider_type: str, config: Dict[str, Any]) -> Dict[str, Any]:
        if provider_type == 'gpt':
            return {"api_key": config.get('OPENAI_API_KEY')}
        elif provider_type == 'claude':
            return {"api_key": config.get('CLAUDE_API_KEY')}
        elif provider_type == 'google':
            return {"api_key": config.get('GOOGLE_API_KEY')}
        elif provider_type == 'ollama':
            return {"host": self.args.get('ollama_host', "http://localhost:11434")}
        else:
            return {}

    def send_message(self, input_data: str, context: str = "") -> str:
        messages = self._prepare_messages(input_data, context)
        try:
            return self.provider.send_message(messages, self.model, self.args)
        except Exception as e:
            raise SpindleException(f"Error sending message: {str(e)}")

    def stream_message(self, input_data: str, context: str = ""):
        messages = self._prepare_messages(input_data, context)
        try:
            for chunk in self.provider.stream_message(messages, self.model, self.args):
                yield chunk
        except Exception as e:
            raise SpindleException(f"Error streaming message: {str(e)}")

    def _prepare_messages(self, input_data: str, context: str) -> List[Dict[str, str]]:
        system_message = self._get_system_message(context)
        user_message = {"role": "user", "content": input_data}
        return [system_message, user_message] if system_message else [user_message]

    def _get_system_message(self, context: str) -> Optional[Dict[str, str]]:
        config = self.config_manager.get_config()
        if not self.pattern:
            return {"role": "system", "content": context} if context else None

        pattern_file = os.path.join(config.get_patterns_dir(), f"{self.pattern}/system.md")
        try:
            with open(pattern_file, "r") as f:
                content = f.read()
                if context:
                    content = f"{context}\n\n{content}"
                return {"role": "system", "content": content}
        except FileNotFoundError:
            raise SpindleException(f"Pattern file not found: {pattern_file}")

    def handle_response(self, response: str):
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
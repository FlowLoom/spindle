import os
from spindle.config import ConfigManager

class Setup:
    def __init__(self):
        self.config = ConfigManager()

    def run(self):
        self._setup_api_keys()

        # TODO: Conduct more tests to ensure the following methods work as expected
        #self._update_patterns()
        #self._update_shell_configs()

    def _setup_api_keys(self):
        api_keys = {
            'OPENAI_API_KEY': 'OpenAI API key',
            'CLAUDE_API_KEY': 'Claude API key',
            'GOOGLE_API_KEY': 'Google API key',
            'YOUTUBE_API_KEY': 'YouTube API key'
        }

        for env_var, description in api_keys.items():
            key = input(f"Enter your {description} (press Enter to skip): ").strip()
            if key:
                self.config.set(env_var, key)

    def _update_patterns(self):
        from spindle.utils.update import Update
        Update().update_patterns()

    def _update_shell_configs(self):
        from spindle.utils.alias import Alias
        Alias().execute()

    def set_default_model(self, model: str):
        self.config.set('DEFAULT_MODEL', model)
        print(f"Default model set to {model}")
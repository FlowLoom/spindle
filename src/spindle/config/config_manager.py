import os
from dotenv import load_dotenv
from typing import List

__All__ = ["ConfigManager"]


class ConfigManager:
    def __init__(self):
        self.config_dir = os.path.expanduser("~/.config/spindle")
        self.env_file = os.path.join(self.config_dir, ".env")
        os.makedirs(self.config_dir, exist_ok=True)
        load_dotenv(self.env_file)

    def get(self, key: str, default: str = None) -> str:
        return os.getenv(key, default)

    def set(self, key: str, value: str):
        with open(self.env_file, "a") as f:
            f.write(f"{key}={value}\n")
        os.environ[key] = value

    def get_config_dir(self) -> str:
        return self.config_dir

    def get_patterns_dir(self) -> str:
        return os.path.join(self.config_dir, "patterns")

    def get_gpt_models(self) -> List[str]:
        # Implementation to fetch GPT models
        pass

    def get_claude_models(self) -> List[str]:
        # Implementation to fetch Claude models
        pass

    def get_google_models(self) -> List[str]:
        # Implementation to fetch Google models
        pass

    def get_ollama_models(self) -> List[str]:
        # Implementation to fetch Ollama models
        pass
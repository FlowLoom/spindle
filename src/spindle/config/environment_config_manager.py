import os
from typing import Any, Optional, Dict
from dotenv import load_dotenv
from spindle.interfaces import IConfigurationManager

__All__ = ["EnvironmentConfigManager"]


class EnvironmentConfigManager(IConfigurationManager):
    def __init__(self):
        self.config_dir = os.path.expanduser("~/.config/spindle")
        self.env_file = os.path.join(self.config_dir, ".env")
        self.config: Dict[str, Any] = {}
        self._ensure_config_dir()
        self.load()

    def _ensure_config_dir(self):
        """Ensure the configuration directory exists."""
        os.makedirs(self.config_dir, exist_ok=True)

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Retrieve a configuration value."""
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        self.config[key] = value
        self.save()

    def load(self) -> None:
        """Load configuration from the .env file."""
        if os.path.exists(self.env_file):
            load_dotenv(self.env_file)
        self.config = dict(os.environ)

    def save(self) -> None:
        """Save the current configuration to the .env file."""
        with open(self.env_file, "w") as f:
            for key, value in self.config.items():
                f.write(f"{key}={value}\n")

    def get_config_dir(self) -> str:
        """Get the configuration directory path."""
        return self.config_dir

    def get_patterns_dir(self) -> str:
        """Get the patterns directory path."""
        return os.path.join(self.config_dir, "patterns")

    def get_all(self) -> Dict[str, Any]:
        """Get all configuration key-value pairs."""
        return self.config.copy()

    def clear(self) -> None:
        """Clear all configuration settings."""
        self.config.clear()
        self.save()

    def exists(self, key: str) -> bool:
        """Check if a configuration key exists."""
        return key in self.config
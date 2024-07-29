from spindle.config.environment_config_manager import EnvironmentConfigManager
from spindle.managers import ModelProviderManager

__All__ = ["ConfigManager"]


class ConfigManager:
    def __init__(self):
        self.config_manager = EnvironmentConfigManager()
        self.model_provider_manager = ModelProviderManager()

    def get_config(self):
        return self.config_manager

    def get_model_provider_manager(self):
        return self.model_provider_manager
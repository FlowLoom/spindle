import configparser


class ConfigManager:
    def __init__(self, config_file=None):
        self.config = configparser.ConfigParser()
        if config_file:
            self.config.read(config_file)

    def get(self, section, key, fallback=None):
        return self.config.get(section, key, fallback=fallback)

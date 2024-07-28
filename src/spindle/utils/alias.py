import os
from spindle.config import ConfigManager

class Alias:
    def __init__(self):
        self.config = ConfigManager()

    def execute(self):
        patterns = os.listdir(self.config.get_patterns_dir())
        bootstrap_file = os.path.join(self.config.get_config_dir(), "spindle-bootstrap.inc")

        with open(bootstrap_file, "w") as f:
            for pattern in patterns:
                f.write(f"alias {pattern}='spindle fabric --pattern {pattern}'\n")

        self._update_shell_configs(bootstrap_file)

    def _update_shell_configs(self, bootstrap_file):
        shell_configs = ['.bashrc', '.bash_profile', '.zshrc']
        home = os.path.expanduser("~")
        source_line = f'if [ -f "{bootstrap_file}" ]; then . "{bootstrap_file}"; fi'

        for config in shell_configs:
            config_path = os.path.join(home, config)
            if os.path.exists(config_path):
                with open(config_path, 'r+') as f:
                    content = f.read()
                    if source_line not in content:
                        f.seek(0, 2)  # Move to the end of the file
                        f.write(f"\n{source_line}\n")
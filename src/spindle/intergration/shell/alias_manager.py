import os
from spindle.config import ConfigManager

__all__ = ['AliasManager']


class AliasManager:
    def __init__(self):
        self.config_manager = ConfigManager()

    def execute(self):
        config = self.config_manager.get_config()
        patterns_dir = config.get_patterns_dir()
        config_dir = config.get_config_dir()

        patterns = self._get_pattern_list(patterns_dir)
        bootstrap_file = os.path.join(config_dir, "spindle-bootstrap.inc")

        self._create_bootstrap_file(bootstrap_file, patterns)
        self._update_shell_configs(bootstrap_file)

    def _get_pattern_list(self, patterns_dir):
        try:
            return [f for f in os.listdir(patterns_dir) if os.path.isdir(os.path.join(patterns_dir, f))]
        except OSError as e:
            print(f"Error accessing patterns directory: {e}")
            return []

    def _create_bootstrap_file(self, bootstrap_file, patterns):
        try:
            with open(bootstrap_file, "w") as f:
                for pattern in patterns:
                    f.write(f"alias {pattern}='spindle fabric --pattern {pattern}'\n")
            print(f"Bootstrap file created: {bootstrap_file}")
        except IOError as e:
            print(f"Error creating bootstrap file: {e}")

    def _update_shell_configs(self, bootstrap_file):
        shell_configs = ['.bashrc', '.bash_profile', '.zshrc']
        home = os.path.expanduser("~")
        source_line = f'if [ -f "{bootstrap_file}" ]; then . "{bootstrap_file}"; fi'

        for config in shell_configs:
            config_path = os.path.join(home, config)
            if os.path.exists(config_path):
                self._update_single_config(config_path, source_line)

    def _update_single_config(self, config_path, source_line):
        try:
            with open(config_path, 'r+') as f:
                content = f.read()
                if source_line not in content:
                    f.seek(0, 2)  # Move to the end of the file
                    f.write(f"\n{source_line}\n")
                    print(f"Updated {config_path}")
                else:
                    print(f"{config_path} already contains the source line")
        except IOError as e:
            print(f"Error updating {config_path}: {e}")

    def remove_aliases(self):
        config = self.config_manager.get_config()
        config_dir = config.get_config_dir()
        bootstrap_file = os.path.join(config_dir, "spindle-bootstrap.inc")

        if os.path.exists(bootstrap_file):
            try:
                os.remove(bootstrap_file)
                print(f"Removed bootstrap file: {bootstrap_file}")
            except OSError as e:
                print(f"Error removing bootstrap file: {e}")

        self._remove_source_lines_from_configs(bootstrap_file)

    def _remove_source_lines_from_configs(self, bootstrap_file):
        shell_configs = ['.bashrc', '.bash_profile', '.zshrc']
        home = os.path.expanduser("~")
        source_line = f'if [ -f "{bootstrap_file}" ]; then . "{bootstrap_file}"; fi'

        for config in shell_configs:
            config_path = os.path.join(home, config)
            if os.path.exists(config_path):
                self._remove_line_from_file(config_path, source_line)

    def _remove_line_from_file(self, file_path, line_to_remove):
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
            with open(file_path, 'w') as f:
                lines = [line for line in lines if line.strip() != line_to_remove.strip()]
                f.writelines(lines)
            print(f"Removed source line from {file_path}")
        except IOError as e:
            print(f"Error updating {file_path}: {e}")

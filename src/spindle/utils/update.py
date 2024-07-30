import os
import shutil
import tempfile
import requests
from spindle.config import ConfigManager
from spindle.exceptions import SpindleException

__all__ = ["Update"]


class Update:
    def __init__(self):
        self.config = ConfigManager().get_config()
        self.repo_zip_url = "https://github.com/flowloom/spindle/archive/refs/heads/main.zip"

    def update_patterns(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, "repo.zip")
            self._download_zip(self.repo_zip_url, zip_path)
            extracted_folder_path = self._extract_zip(zip_path, temp_dir)
            patterns_source_path = os.path.join(extracted_folder_path, "fabric-main", "patterns")

            if os.path.exists(patterns_source_path):
                self._update_pattern_directory(patterns_source_path)
                print("Patterns updated successfully.")
            else:
                raise SpindleException("Patterns folder not found in the downloaded zip.")

    def _download_zip(self, url: str, save_path: str):
        response = requests.get(url)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(response.content)

    def _extract_zip(self, zip_path: str, extract_to: str):
        import zipfile
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        return extract_to

    def _update_pattern_directory(self, source_path: str):
        pattern_dir = self.config.get_patterns_dir()
        if os.path.exists(pattern_dir):
            self._backup_custom_patterns(pattern_dir, source_path)
            shutil.rmtree(pattern_dir)
        shutil.copytree(source_path, pattern_dir)

    def _backup_custom_patterns(self, current_dir: str, new_dir: str):
        current_patterns = set(os.listdir(current_dir))
        new_patterns = set(os.listdir(new_dir))
        custom_patterns = current_patterns - new_patterns
        for pattern in custom_patterns:
            shutil.move(os.path.join(current_dir, pattern), new_dir)

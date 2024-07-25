import os
import logging
from typing import Dict, List
from ct.abstracts import AbstractFileParser


class CodeParser(AbstractFileParser):
    """Parses files in a source directory based on exclusion rules and file extensions."""

    def is_valid_file(self, file: str) -> bool:
        """Determines if a file should be processed based on exclusion rules and extensions."""
        return file not in self.excluded_files

    def is_valid_dir(self, dir: str) -> bool:
        """Determines if a directory should be processed based on exclusion rules."""
        return dir not in self.excluded_dirs

    def is_valid_extension(self, file: str) -> bool:
        """Determines if a file should be processed based on its extension."""
        return any(file.endswith(ext) for ext in self.file_extensions)

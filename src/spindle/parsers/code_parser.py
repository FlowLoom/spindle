import os
import logging
from typing import Dict, List
from spindle.abstracts import AbstractFileParser

__All__ = ["CodeParser"]


class CodeParser(AbstractFileParser):
    """
    Parses files in a source directory based on exclusion rules and file extensions.

    This class extends AbstractFileParser to provide specific file parsing functionality
    for code files, considering exclusion rules and allowed file extensions.
    """

    def is_valid_file(self, file: str) -> bool:
        """
        Determines if a file should be processed based on exclusion rules.

        Args:
            file (str): The name of the file to check.

        Returns:
            bool: True if the file should be processed, False otherwise.
        """
        return file not in self.excluded_files

    def is_valid_dir(self, dir: str) -> bool:
        """
        Determines if a directory should be processed based on exclusion rules.

        Args:
            dir (str): The name of the directory to check.

        Returns:
            bool: True if the directory should be processed, False otherwise.
        """
        return dir not in self.excluded_dirs

    def is_valid_extension(self, file: str) -> bool:
        """
        Determines if a file should be processed based on its extension.

        Args:
            file (str): The name of the file to check.

        Returns:
            bool: True if the file has a valid extension, False otherwise.
        """
        return any(file.endswith(ext) for ext in self.file_extensions)

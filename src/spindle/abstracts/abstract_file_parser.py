from spindle.interfaces import IParser, IProcessor
from abc import abstractmethod
from typing import Dict, List
import os
import logging

__All__ = ["AbstractFileParser"]


class AbstractFileParser(IParser):
    """Abstract class for file parsers."""
    def __init__(
            self,
            processor: IProcessor,
            src_folder: str,
            excluded_dirs: List[str],
            excluded_files: List[str],
            file_extensions: List[str]
    ):
        self.processor = processor
        self.src_folder = src_folder
        self.excluded_dirs = excluded_dirs
        self.excluded_files = excluded_files
        self.file_extensions = file_extensions

    def parse(self) -> Dict[str, List[str]]:
        """Parses files in the src directory."""
        parsed_files = {}

        for root, dirs, files in os.walk(self.src_folder):
            dirs[:] = [d for d in dirs if self.is_valid_dir(d)]
            for file in files:
                if not self.is_valid_file(file) or not self.is_valid_extension(file):
                    logging.info(f"Skipping file: {file}")
                    continue
                module_path = os.path.join(root, file)
                logging.info(f"Processing file: {file}")
                content = self.processor.process(module_path)
                parsed_files[module_path] = content

        return parsed_files

    @abstractmethod
    def is_valid_file(self, file: str) -> bool:
        """Determines if a file should be processed based on exclusion rules and extensions."""
        pass

    @abstractmethod
    def is_valid_dir(self, dir: str) -> bool:
        """Determines if a directory should be processed based on exclusion rules."""
        pass

    def is_valid_extension(self, file: str) -> bool:
        """Determines if a file should be processed based on its extension."""
        pass
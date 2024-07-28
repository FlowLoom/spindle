import os
from typing import Any, Dict, List
from spindle.abstracts import AbstractParser
from spindle.interfaces import IProcessor, IVisitor

class CodeParser(AbstractParser):
    def __init__(self, processor: IProcessor, excluded_dirs: List[str], excluded_files: List[str], file_extensions: List[str]):
        super().__init__(processor)
        self.excluded_dirs = excluded_dirs
        self.excluded_files = excluded_files
        self.file_extensions = file_extensions

    def _fetch_content(self, source: str) -> Dict[str, str]:
        """
        Fetch all valid file contents from the source directory.

        Args:
            source (str): The source directory path.

        Returns:
            Dict[str, str]: A dictionary mapping file paths to their content.
        """
        content = {}
        for root, dirs, files in os.walk(source):
            dirs[:] = [d for d in dirs if self._is_valid_dir(d)]
            for file in files:
                if self._is_valid_file(file) and self._is_valid_extension(file):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content[file_path] = f.read()
        return content

    def _format_output(self, processed_content: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """
        Format the processed content. In this case, we're just returning it as is.

        Args:
            processed_content (Dict[str, List[str]]): The processed content to format.

        Returns:
            Dict[str, List[str]]: The formatted output.
        """
        return processed_content

    def accept(self, visitor: IVisitor) -> None:
        """
        Accept a visitor to perform operations on this parser.

        Args:
            visitor (IVisitor): The visitor to accept
        """
        visitor.visit(self)

    def _is_valid_dir(self, dir: str) -> bool:
        """
        Check if a directory should be included in parsing.

        Args:
            dir (str): The directory name.

        Returns:
            bool: True if the directory should be included, False otherwise.
        """
        return dir not in self.excluded_dirs

    def _is_valid_file(self, file: str) -> bool:
        """
        Check if a file should be included in parsing.

        Args:
            file (str): The file name.

        Returns:
            bool: True if the file should be included, False otherwise.
        """
        return file not in self.excluded_files

    def _is_valid_extension(self, file: str) -> bool:
        """
        Check if a file has a valid extension for parsing.

        Args:
            file (str): The file name.

        Returns:
            bool: True if the file has a valid extension, False otherwise.
        """
        return any(file.endswith(ext) for ext in self.file_extensions)
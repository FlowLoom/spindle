import os
from typing import Any, Dict, List
from spindle.abstracts import AbstractParser
from spindle.interfaces import IProcessor

__All__ = ['CodeParser']

class CodeParser(AbstractParser):
    """
    A parser for code files that extends AbstractParser.

    This class implements parsing logic for code files, including file traversal,
    content extraction, and processing using a provided processor.

    Attributes:
        excluded_dirs (List[str]): Directories to exclude from parsing.
        excluded_files (List[str]): Files to exclude from parsing.
        file_extensions (List[str]): Valid file extensions for parsing.
    """

    def __init__(self, processor: IProcessor, excluded_dirs: List[str], excluded_files: List[str], file_extensions: List[str]):
        """
        Initialize the CodeParser with a processor and parsing criteria.

        Args:
            processor (IProcessor): The processor to use for content processing.
            excluded_dirs (List[str]): Directories to exclude from parsing.
            excluded_files (List[str]): Files to exclude from parsing.
            file_extensions (List[str]): Valid file extensions for parsing.
        """

        super().__init__(processor)
        self.excluded_dirs = excluded_dirs
        self.excluded_files = excluded_files
        self.file_extensions = file_extensions

    def _fetch_content(self, source: str) -> List[str]:
        """
        Fetch all valid file paths from the source directory.

        This method walks through the directory tree, filtering out excluded
        directories and files, and collects paths of files with valid extensions.

        Args:
            source (str): The source directory path.

        Returns:
            List[str]: A list of valid file paths.
        """

        file_paths = []
        for root, dirs, files in os.walk(source):

            # Filter out excluded directories
            dirs[:] = [d for d in dirs if self._is_valid_dir(d)]
            for file in files:
                if self._is_valid_file(file) and self._is_valid_extension(file):
                    file_paths.append(os.path.join(root, file))
        return file_paths

    def _extract_content(self, file_paths: List[str]) -> Dict[str, str]:
        """
        Extract content from each file path.

        This method reads the content of each file and stores it in a dictionary.

        Args:
            file_paths (List[str]): List of file paths to extract content from.

        Returns:
            Dict[str, str]: A dictionary mapping file paths to their content.
        """

        content_dict = {}
        for file_path in file_paths:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                content_dict[file_path] = file.read()
        return content_dict

    def _process_content(self, content: Dict[str, str]) -> Dict[str, List[str]]:
        """
        Process the content of each file using the processor.

        This method applies the processor to the content of each file.

        Args:
            content (Dict[str, str]): A dictionary mapping file paths to their content.

        Returns:
            Dict[str, List[str]]: A dictionary mapping file paths to their processed content.
        """

        processed_content = {}
        for file_path, file_content in content.items():
            processed_content[file_path] = self.processor.process(file_content)
        return processed_content

    def _format_output(self, processed_content: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """
        Format the processed content.

        In this implementation, the method returns the processed content as is.

        Args:
            processed_content (Dict[str, List[str]]): The processed content to format.

        Returns:
            Dict[str, List[str]]: The formatted output.
        """

        return processed_content

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

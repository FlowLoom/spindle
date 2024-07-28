# In spindle/factories/code_parser_factory.py

from spindle.abstracts import AbstractParserFactory
from spindle.parsers import CodeParser
from spindle.processors import CodeProcessor
from spindle.handlers import FileHandler, ConsolePrintHandler
from spindle.interfaces import IHandler, IProcessor
from typing import List, Optional

__All__ = ['CodeParserFactory']


class CodeParserFactory(AbstractParserFactory):
    """
    A factory class for creating code parsing components.

    This class provides methods to create and configure CodeParser instances,
    along with associated processors and handlers. It also manages default
    settings for excluded directories, files, and file extensions.
    """

    def __init__(self):
        """
        Initialize the CodeParserFactory with default settings.
        """

        self.default_excluded_dirs = ['venv', '.git', '__pycache__']
        self.default_excluded_files = ['setup.py', 'requirements.txt']
        self.default_file_extensions = ['.py', '.js', '.html', '.css']

    def _create_parser(self, *args, **kwargs) -> CodeParser:
        """
        Create and return a CodeParser instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            CodeParser: An instance of CodeParser configured with the specified
                        or default settings.
        """

        processor = self.create_processor(**kwargs)
        excluded_dirs = kwargs.get('excluded_dirs', self.default_excluded_dirs)
        excluded_files = kwargs.get('excluded_files', self.default_excluded_files)
        file_extensions = kwargs.get('file_extensions', self.default_file_extensions)

        return CodeParser(processor, excluded_dirs, excluded_files, file_extensions)

    def _create_processor(self, **kwargs) -> IProcessor:
        """
        Create and return a CodeProcessor instance.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            IProcessor: An instance of CodeProcessor configured with the specified
                        or default settings.
        """

        remove_comments = kwargs.get('remove_comments', True)
        remove_empty_lines = kwargs.get('remove_empty_lines', True)
        trim_lines = kwargs.get('trim_lines', True)

        return CodeProcessor(remove_comments, remove_empty_lines, trim_lines)

    def _create_handler(self, *args, **kwargs) -> IHandler:
        """
        Create and return an appropriate handler instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            IHandler: An instance of a concrete handler (ConsolePrintHandler or FileHandler)
                      based on the provided arguments.
        """

        if kwargs.get('console') or kwargs.get('con'):
            return ConsolePrintHandler()
        elif 'output' in kwargs and kwargs['output'] is not None:
            return FileHandler(kwargs['output'])
        else:
            return ConsolePrintHandler()

    def set_default_excluded_dirs(self, dirs: List[str]) -> None:
        """
        Set the default excluded directories.

        Args:
            dirs (List[str]): List of directory names to exclude.
        """

        self.default_excluded_dirs = dirs

    def set_default_excluded_files(self, files: List[str]) -> None:
        """
        Set the default excluded files.

        Args:
            files (List[str]): List of file names to exclude.
        """

        self.default_excluded_files = files

    def set_default_file_extensions(self, extensions: List[str]) -> None:
        """
        Set the default file extensions to include.

        Args:
            extensions (List[str]): List of file extensions to include.
        """

        self.default_file_extensions = extensions

    def add_excluded_dir(self, dir: str) -> None:
        """
        Add a directory to the default excluded directories list.

        Args:
            dir (str): Directory name to exclude.
        """

        if dir not in self.default_excluded_dirs:
            self.default_excluded_dirs.append(dir)

    def add_excluded_file(self, file: str) -> None:
        """
        Add a file to the default excluded files list.

        Args:
            file (str): File name to exclude.
        """

        if file not in self.default_excluded_files:
            self.default_excluded_files.append(file)

    def add_file_extension(self, extension: str) -> None:
        """
        Add a file extension to the default file extensions list.

        Args:
            extension (str): File extension to include.
        """

        if extension not in self.default_file_extensions:
            self.default_file_extensions.append(extension)
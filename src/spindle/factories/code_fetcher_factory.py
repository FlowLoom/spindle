from spindle.abstracts import AbstractFetcherFactory
from spindle.fetchers import CodeFetcher
from spindle.processors import CodeProcessor
from spindle.handlers import FileHandler, ConsoleHandler
from spindle.serializers import ISerializer
from spindle.factories import SerializerFactory
from spindle.interfaces import IHandler, IFetcher
from typing import List, Optional

__All__ = ['CodeFetcherFactory']


class CodeFetcherFactory(AbstractFetcherFactory):
    def __init__(self):
        self.default_excluded_dirs = ['venv', '.git', '__pycache__']
        self.default_excluded_files = ['setup.py', 'requirements.txt']
        self.default_file_extensions = ['.py', '.js', '.html', '.css']
        self.serializer_factory = SerializerFactory()

    def _create_fetcher(self, remove_comments: bool = True, remove_empty_lines: bool = True,
                       trim_lines: bool = True, **kwargs) -> IFetcher:
        processor = self._create_processor(remove_comments, remove_empty_lines, trim_lines)
        return CodeFetcher(processor,
                           self.default_excluded_dirs,
                           self.default_excluded_files,
                           self.default_file_extensions)

    def _create_handler(self, handler_type: str, format: str = 'plaintext', **kwargs) -> IHandler:
        serializer = self.serializer_factory.create_serializer(format)

        if handler_type.lower() == 'file':
            return FileHandler(serializer, kwargs.get('output_file', 'output.txt'))
        elif handler_type.lower() == 'console':
            console_handler = ConsoleHandler(serializer)
            if 'color' in kwargs:
                console_handler.set_color(kwargs['color'])
            return console_handler
        else:
            raise ValueError(f"Unsupported handler type: {handler_type}")

    def _create_processor(self, remove_comments: bool, remove_empty_lines: bool, trim_lines: bool) -> CodeProcessor:
        return CodeProcessor(remove_comments, remove_empty_lines, trim_lines)

    def set_default_excluded_dirs(self, dirs: List[str]) -> None:
        self.default_excluded_dirs = dirs

    def set_default_excluded_files(self, files: List[str]) -> None:
        self.default_excluded_files = files

    def set_default_file_extensions(self, extensions: List[str]) -> None:
        self.default_file_extensions = extensions

    def add_excluded_dir(self, dir: str) -> None:
        if dir not in self.default_excluded_dirs:
            self.default_excluded_dirs.append(dir)

    def add_excluded_file(self, file: str) -> None:
        if file not in self.default_excluded_files:
            self.default_excluded_files.append(file)

    def add_file_extension(self, extension: str) -> None:
        if extension not in self.default_file_extensions:
            self.default_file_extensions.append(extension)
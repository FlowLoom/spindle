from spindle.abstracts import AbstractProcessor
from typing import List, Dict, Any
import re

__All__ = ['CodeProcessor']


class CodeProcessor(AbstractProcessor):
    def __init__(self,
                 remove_comments: bool = True,
                 remove_empty_lines: bool = True,
                 trim_lines: bool = True,
                 min_line_length: int = 0,
                 max_line_length: int = None):
        self.remove_comments = remove_comments
        self.remove_empty_lines = remove_empty_lines
        self.trim_lines = trim_lines
        self.min_line_length = min_line_length
        self.max_line_length = max_line_length

    def _preprocess(self, content: Dict[str, str], **kwargs: Any) -> Dict[str, str]:
        """
        Preprocess the code content.
        In this case, we're not doing any preprocessing before extraction.
        """
        return self._extract_content(content)

    def _extract_content(self, content: Dict[str, str], **kwargs: Any) -> Dict[str, List[str]]:
        """
        Extract content by splitting each file's content into lines.
        """
        return {file_path: content.split('\n') for file_path, content in content.items()}

    def _main_process(self, content: Dict[str, List[str]], **kwargs: Any) -> Dict[str, List[str]]:
        """
        Main processing step for the code content.
        """
        processed_content = {}
        for file_path, lines in content.items():
            processed_lines = []
            for line in lines:
                if self.trim_lines:
                    line = line.strip()

                if self.remove_comments:
                    line = self._remove_comments(line)

                if (not self.remove_empty_lines or line) and len(line) >= self.min_line_length:
                    if self.max_line_length and len(line) > self.max_line_length:
                        line = line[:self.max_line_length] + '...'
                    processed_lines.append(line)

            processed_content[file_path] = processed_lines

        return processed_content

    def _postprocess(self, content: Dict[str, List[str]], **kwargs: Any) -> Dict[str, List[str]]:
        """
        Postprocess the code content.
        In this case, we're just returning the processed content as is.
        """
        return content

    def _remove_comments(self, line: str) -> str:
        """
        Remove comments from a line of code.
        """
        # Remove inline comments
        line = re.sub(r'#.*$', '', line)

        # Remove full-line comments
        if line.lstrip().startswith('#'):
            return ''

        return line

    @staticmethod
    def remove_non_ascii(text: str) -> str:
        """
        Remove non-ASCII characters from a string.
        """
        return text.encode("ascii", errors="ignore").decode("ascii")

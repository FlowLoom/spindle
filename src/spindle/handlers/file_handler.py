from typing import Dict, List
from spindle.abstracts import AbstractHandler

__All__ = ["FileHandler"]


class FileHandler(AbstractHandler):
    """Handles the parsed files' content by writing them to a file."""

    def __init__(self, output_file: str):
        self.output_file = output_file

    def handle(self, parsed_files: Dict[str, List[str]]) -> None:
        """Writes the parsed files' content to the specified output file.

        Args:
            parsed_files (Dict[str, List[str]]): A dictionary where the key is the file name and the value is a list of strings representing the file's content.
        """
        with open(self.output_file, "w", encoding="utf-8") as out_file:
            for file_name, content in parsed_files.items():
                out_file.write(f"{file_name}:\n")
                for line in content:
                    out_file.write(line + "\n")
                out_file.write("\n" + "="*40 + "\n")

from typing import Dict, List
from spindle.abstracts import AbstractHandler

__All__ = ["ConsolePrintHandler"]


class ConsolePrintHandler(AbstractHandler):
    """Handles the parsed files' content by printing them to the console."""

    def handle(self, parsed_files: Dict[str, List[str]]) -> None:
        """Prints the parsed files' content to the console.

        Args:
            parsed_files (Dict[str, List[str]]): A dictionary where the key is the file name and the value is a list of strings representing the file's content.
        """
        for item, content in parsed_files.items():
            print(f"{item}")
            for line in content:
                print(line)
            print("\n" + "="*40 + "\n")

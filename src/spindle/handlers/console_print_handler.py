from typing import Dict, List
from spindle.abstracts import AbstractHandler

__All__ = ["ConsolePrintHandler"]


class ConsolePrintHandler(AbstractHandler):
    """
    Handles the parsed files' content by printing them to the console.

    This class implements the AbstractHandler interface to provide
    functionality for displaying parsed file contents in a formatted
    manner on the console output.
    """

    def handle(self, parsed_files: Dict[str, List[str]]) -> None:
        """
        Prints the parsed files' content to the console.

        Iterates through the provided dictionary of parsed files,
        displaying each file's name followed by its content, with
        a separator line between files.

        Args:
            parsed_files (Dict[str, List[str]]): A dictionary where
                the key is the file name and the value is a list of
                strings representing the file's content.

        Returns:
            None
        """
        for item, content in parsed_files.items():
            # Print the file name
            print(f"{item}")

            # Print each line of the file's content
            for line in content:
                print(line)

            # Print a separator line between files
            print("\n" + "="*40 + "\n")

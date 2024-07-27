from typing import Dict, List
from spindle.abstracts import AbstractHandler

__All__ = ["FileHandler"]


class FileHandler(AbstractHandler):
    """
    Handles the parsed files' content by writing them to a file.

    This class inherits from AbstractHandler and provides functionality
    to write parsed file contents to a specified output file.
    """

    def __init__(self, output_file: str):
        """
        Initialize the FileHandler with the specified output file.

        Args:
            output_file (str): The path to the file where parsed content will be written.
        """
        self.output_file = output_file

    def handle(self, parsed_files: Dict[str, List[str]]) -> None:
        """
        Writes the parsed files' content to the specified output file.

        This method iterates through the parsed files dictionary, writing each file's
        name followed by its content to the output file. A separator line is added
        between each file's content for better readability.

        Args:
            parsed_files (Dict[str, List[str]]): A dictionary where the key is the file name
                and the value is a list of strings representing the file's content.

        Returns:
            None

        Raises:
            IOError: If there's an issue writing to the output file.
        """
        with open(self.output_file, "w", encoding="utf-8") as out_file:
            for file_name, content in parsed_files.items():
                # Write the file name as a header
                out_file.write(f"{file_name}:\n")

                # Write each line of the file's content
                for line in content:
                    out_file.write(line + "\n")

                # Add a separator line between files
                out_file.write("\n" + "="*40 + "\n")

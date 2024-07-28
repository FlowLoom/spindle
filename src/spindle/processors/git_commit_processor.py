from typing import Any, List, Dict, Optional
import re
from spindle.abstracts import AbstractProcessor

_ALL__ = ['GitCommitProcessor']


class GitCommitProcessor(AbstractProcessor):
    """
    A processor for git commit messages with customizable options.

    This class provides functionality to process git commit messages, including
    ticket number extraction, message length limitation, and first word capitalization.

    Attributes:
        extract_ticket_number (bool): Flag to enable ticket number extraction.
        max_length (int): Maximum allowed length for the commit message.
        capitalize_first_word (bool): Flag to enable first word capitalization.
    """

    def __init__(self, extract_ticket_number: bool = False, max_length: int = 72, capitalize_first_word: bool = True):
        """
        Initialize the GitCommitProcessor with customizable options.

        Args:
            extract_ticket_number (bool, optional): Enable ticket number extraction. Defaults to False.
            max_length (int, optional): Maximum allowed length for the commit message. Defaults to 72.
            capitalize_first_word (bool, optional): Enable first word capitalization. Defaults to True.
        """

        self.extract_ticket_number = extract_ticket_number
        self.max_length = max_length
        self.capitalize_first_word = capitalize_first_word

    def process(self, content: str) -> Any:
        """
        Process the given git commit message content.

        This method overrides the superclass method to handle git commit message processing.

        Args:
            content (str): The git commit message to be processed.

        Returns:
            Any: The processed git commit message.
        """

        return super().process(content)

    def _preprocess(self, content: str) -> str:
        """
        Preprocess the git commit message.

        This method removes any leading or trailing whitespace from the commit message.

        Args:
            content (str): The git commit message to be preprocessed.

        Returns:
            str: The preprocessed git commit message.
        """

        # Remove any leading or trailing whitespace
        return content.strip()

    def _main_process(self, content: str) -> Dict[str, Any]:
        """
        Main processing step for the git commit message.

        This method handles ticket number extraction, message length limitation,
        and first word capitalization based on the processor's configuration.

        Args:
            content (str): The git commit message to be processed.

        Returns:
            Dict[str, Any]: A dictionary containing the processed commit message and any extracted information.
        """

        result = {"message": content}

        if self.extract_ticket_number:
            ticket_number = self._extract_ticket_number(content)
            if ticket_number:
                result["ticket_number"] = ticket_number

        # Truncate the message if it's longer than max_length
        if len(content) > self.max_length:
            result["message"] = content[:self.max_length] + "..."

        if self.capitalize_first_word:
            result["message"] = self._capitalize_first_word(result["message"])

        return result

    def _postprocess(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Postprocess the git commit message.

        This method is a placeholder for any final processing steps.
        Currently, it returns the input content unchanged.

        Args:
            content (Dict[str, Any]): The processed git commit message and extracted information.

        Returns:
            Dict[str, Any]: The postprocessed git commit message and information.
        """

        # In this case, we're just returning the content as is
        return content

    def _extract_ticket_number(self, message: str) -> Optional[str]:
        """
        Extract a ticket number from the commit message.

        This method uses a regular expression to find patterns like "JIRA-123" or "#123" in the commit message.

        Args:
            message (str): The commit message.

        Returns:
            Optional[str]: The extracted ticket number, if found; otherwise, None.
        """

        # This regex looks for patterns like "JIRA-123" or "#123"
        match = re.search(r'([A-Z]+-\d+|#\d+)', message)
        return match.group(1) if match else None

    @staticmethod
    def _capitalize_first_word(message: str) -> str:
        """
        Capitalize the first word of the commit message.

        This method capitalizes the first character of the commit message, leaving the rest unchanged.

        Args:
            message (str): The commit message.

        Returns:
            str: The commit message with the first word capitalized.
        """

        return message[0].upper() + message[1:]

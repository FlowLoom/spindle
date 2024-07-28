from typing import Any, List, Dict, Optional
import re
from spindle.abstracts import AbstractProcessor

__All__ = ["GitCommitProcessor"]


class GitCommitProcessor(AbstractProcessor):
    def __init__(self, extract_ticket_number: bool = False, max_length: int = 72, capitalize_first_word: bool = True):
        self.extract_ticket_number = extract_ticket_number
        self.max_length = max_length
        self.capitalize_first_word = capitalize_first_word

    def _preprocess(self, content: List[Any]) -> List[Any]:
        """
        Preprocess the git commit messages.
        In this case, we're not doing any preprocessing before extraction.
        """
        return self._extract_content(content)

    def _extract_content(self, commits: List[Any]) -> List[str]:
        """
        Extract the commit messages from the commit objects.
        """
        return [commit.message.strip() for commit in commits]

    def _main_process(self, commit_messages: List[str]) -> List[Dict[str, Any]]:
        """
        Main processing step for the git commit messages.
        """
        processed_commits = []
        for message in commit_messages:
            processed_commit = {"message": message}

            if self.extract_ticket_number:
                ticket_number = self._extract_ticket_number(message)
                if ticket_number:
                    processed_commit["ticket_number"] = ticket_number

            if len(message) > self.max_length:
                processed_commit["message"] = message[:self.max_length] + "..."

            if self.capitalize_first_word:
                processed_commit["message"] = self._capitalize_first_word(processed_commit["message"])

            processed_commits.append(processed_commit)

        return processed_commits

    def _postprocess(self, processed_commits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Postprocess the git commit messages.
        In this case, we're just returning the processed commits as is.
        """
        return processed_commits

    def _extract_ticket_number(self, message: str) -> Optional[str]:
        """
        Extract a ticket number from the commit message.
        """
        match = re.search(r'([A-Z]+-\d+|#\d+)', message)
        return match.group(1) if match else None

    @staticmethod
    def _capitalize_first_word(message: str) -> str:
        """
        Capitalize the first word of the commit message.
        """
        return message[0].upper() + message[1:]

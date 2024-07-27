from typing import Any, Dict, List, Optional
from spindle.abstracts import AbstractGitParser
from git import Repo

__All__ = ['GitCommitParser']


class GitCommitParser(AbstractGitParser):
    """
    A parser for extracting and processing Git commit messages.

    This class implements the AbstractGitParser interface and provides
    methods for parsing commit messages, counting commits, and retrieving
    specific commits by hash.
    """

    def parse(self, source: Any, start: Optional[int] = None, end: Optional[int] = None) -> Dict[str, List[str]]:
        """
        Parse commit messages from a Git repository.

        Args:
            source (Any): The path to the Git repository.
            start (Optional[int]): The starting index for commit range (inclusive).
            end (Optional[int]): The ending index for commit range (exclusive).

        Returns:
            Dict[str, List[str]]: A dictionary mapping commit hashes to processed commit messages.
        """

        commit_messages = {}
        repo_path = source
        repo = Repo(repo_path)
        commits = list(repo.iter_commits())

        # Handle commit range
        if start is not None and end is not None:
            commits = commits[start:end]

        for commit in commits:
            commit_hash = commit.hexsha
            message = commit.message.strip()
            processed_message = self.process_commit_message(message)
            commit_messages[commit_hash] = processed_message

        return commit_messages

    def process_commit_message(self, commit_message: str) -> List[str]:
        """
        Process a single commit message.

        Args:
            commit_message (str): The commit message to process.

        Returns:
            List[str]: A list containing the processed commit message.
        """
        return [commit_message]

    def get_commit_count(self, source: Any) -> int:
        """
        Get the total number of commits in a Git repository.

        Args:
            source (Any): The path to the Git repository.

        Returns:
            int: The total number of commits.
        """
        repo_path = source
        repo = Repo(repo_path)
        return sum(1 for _ in repo.iter_commits())

    def get_commit_by_hash(self, source: Any, hash_prefix: str) -> Optional[Dict[str, List[str]]]:
        """
        Retrieve a specific commit by its hash prefix.

        Args:
            source (Any): The path to the Git repository.
            hash_prefix (str): The prefix of the commit hash to search for.

        Returns:
            Optional[Dict[str, List[str]]]: A dictionary containing the commit hash and processed message,
                                            or None if no matching commit is found.
        """
        repo_path = source
        repo = Repo(repo_path)
        for commit in repo.iter_commits():
            if commit.hexsha.startswith(hash_prefix):
                commit_hash = commit.hexsha
                message = commit.message.strip()
                processed_message = self.process_commit_message(message)
                return {commit_hash: processed_message}
        return None

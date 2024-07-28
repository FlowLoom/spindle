# In spindle/parsers/git_commit_parser.py

from typing import Any, Dict, List, Optional
from git import Repo, Commit
from spindle.abstracts import AbstractParser
from spindle.interfaces import IProcessor

__ALL__ = ["GitCommitParser"]


class GitCommitParser(AbstractParser):
    """
    A parser for extracting and processing git commit messages from a repository.

    This class extends AbstractParser and provides methods to fetch, extract,
    process, and format git commit messages.
    """

    def __init__(self, processor: IProcessor):
        """
        Initialize the GitCommitParser with a processor.

        Args:
            processor (IProcessor): The processor to use for commit message processing.
        """

        super().__init__(processor)

    def parse(self, source: str, start: Optional[int] = None, end: Optional[int] = None) -> Dict[str, List[str]]:
        """
        Parse git commit messages from the given repository.

        Args:
            source (str): Path to the git repository.
            start (Optional[int]): Start index for commit range (inclusive).
            end (Optional[int]): End index for commit range (exclusive).

        Returns:
            Dict[str, List[str]]: A dictionary with 'commits' key containing processed commit messages.
        """

        raw_content = self._fetch_content(source)
        extracted_content = self._extract_content(raw_content, start, end)
        processed_content = self._process_content(extracted_content)
        return self._format_output(processed_content)

    def _fetch_content(self, source: str) -> Repo:
        """
        Fetch the git repository.

        Args:
            source (str): Path to the git repository.

        Returns:
            Repo: A git.Repo object representing the repository.
        """
        return Repo(source)

    def _extract_content(self, repo: Repo, start: Optional[int] = None, end: Optional[int] = None) -> List[Commit]:
        """
        Extract commits from the repository.

        Args:
            repo (Repo): The git repository object.
            start (Optional[int]): Start index for commit range (inclusive).
            end (Optional[int]): End index for commit range (exclusive).

        Returns:
            List[Commit]: A list of git.Commit objects.
        """

        commits = list(repo.iter_commits())
        if start is not None and end is not None:
            commits = commits[start:end]
        elif start is not None:
            commits = commits[start:]
        elif end is not None:
            commits = commits[:end]
        return commits

    def _process_content(self, commits: List[Commit]) -> List[str]:
        """
        Process the commit messages using the associated processor.

        Args:
            commits (List[Commit]): A list of git.Commit objects.

        Returns:
            List[str]: A list of processed commit messages.
        """

        return [self.processor.process(commit.message.strip()) for commit in commits]

    def _format_output(self, processed_commits: List[str]) -> Dict[str, List[str]]:
        """
        Format the processed commits into the expected output structure.

        Args:
            processed_commits (List[str]): A list of processed commit messages.

        Returns:
            Dict[str, List[str]]: A dictionary with 'commits' key containing the processed commit messages.
        """

        return {"commits": processed_commits}

    def get_commit_count(self, source: str) -> int:
        """
        Get the total number of commits in the repository.

        Args:
            source (str): Path to the git repository.

        Returns:
            int: The total number of commits.
        """

        repo = self._fetch_content(source)
        return sum(1 for _ in repo.iter_commits())

    def get_commit_by_hash(self, source: str, hash_prefix: str) -> Optional[Dict[str, List[str]]]:
        """
        Retrieve a specific commit by its hash prefix.

        Args:
            source (str): Path to the git repository.
            hash_prefix (str): The prefix of the commit hash to search for.

        Returns:
            Optional[Dict[str, List[str]]]: A dictionary containing the commit hash and processed message,
                                            or None if no matching commit is found.
        """

        repo = self._fetch_content(source)
        for commit in repo.iter_commits():
            if commit.hexsha.startswith(hash_prefix):
                processed_message = self.processor.process(commit.message.strip())
                return {commit.hexsha: processed_message}
        return None
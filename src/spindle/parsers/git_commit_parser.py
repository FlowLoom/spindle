# In spindle/parsers/git_commit_parser.py

from typing import Any, Dict, List, Optional, Union
from git import Repo, Commit
from spindle.abstracts import AbstractParser
from spindle.interfaces import IProcessor, IVisitor

class GitCommitParser(AbstractParser):
    def __init__(self, processor: IProcessor):
        super().__init__(processor)

    def parse(self, source: str, start: Optional[int] = None, end: Optional[int] = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        Parse git commit messages from the given repository.

        Args:
            source (str): Path to the git repository.
            start (Optional[int]): Start index for commit range (inclusive).
            end (Optional[int]): End index for commit range (exclusive).

        Returns:
            Dict[str, List[Dict[str, Any]]]: A dictionary with 'commits' key containing processed commit messages.
        """
        raw_content = self._fetch_content(source, start, end)
        processed_content = self._process_content(raw_content)
        return self._format_output(processed_content)

    def _fetch_content(self, source: str, start: Optional[int] = None, end: Optional[int] = None) -> List[Commit]:
        """
        Fetch commits from the git repository.

        Args:
            source (str): Path to the git repository.
            start (Optional[int]): Start index for commit range (inclusive).
            end (Optional[int]): End index for commit range (exclusive).

        Returns:
            List[Commit]: A list of git.Commit objects.
        """
        repo = Repo(source)
        commits = list(repo.iter_commits())
        return self._get_commits_by_range(commits, start, end)

    def _get_commits_by_range(self, commits: List[Commit], start: Optional[int] = None, end: Optional[int] = None) -> List[Commit]:
        """
        Get commits within the specified range.

        Args:
            commits (List[Commit]): List of all commits.
            start (Optional[int]): Start index for commit range (inclusive).
            end (Optional[int]): End index for commit range (exclusive).

        Returns:
            List[Commit]: A list of commits within the specified range.
        """
        if start is not None and end is not None:
            return commits[start:end]
        elif start is not None:
            return commits[start:]
        elif end is not None:
            return commits[:end]
        return commits

    def _format_output(self, processed_content: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Format the processed commits into the expected output structure.

        Args:
            processed_content (List[Dict[str, Any]]): A list of processed commit dictionaries.

        Returns:
            Dict[str, List[Dict[str, Any]]]: A dictionary with 'commits' key containing the processed commits.
        """
        return {"commits": processed_content}

    def accept(self, visitor: IVisitor) -> None:
        """
        Accept a visitor to perform operations on this parser.

        Args:
            visitor (IVisitor): The visitor to accept
        """
        visitor.visit(self)

    def get_commit_count(self, source: str) -> int:
        """
        Get the total number of commits in the repository.

        Args:
            source (str): Path to the git repository.

        Returns:
            int: The total number of commits.
        """
        repo = Repo(source)
        return sum(1 for _ in repo.iter_commits())

    def get_commit_by_hash(self, source: str, hash_prefix: str) -> Optional[Dict[str, List[Dict[str, Any]]]]:
        """
        Retrieve a specific commit by its hash prefix.

        Args:
            source (str): Path to the git repository.
            hash_prefix (str): The prefix of the commit hash to search for.

        Returns:
            Optional[Dict[str, List[Dict[str, Any]]]]: A dictionary containing the commit hash and processed message,
                                                       or None if no matching commit is found.
        """
        repo = Repo(source)
        for commit in repo.iter_commits():
            if commit.hexsha.startswith(hash_prefix):
                processed_commit = self._process_content([commit])
                return {commit.hexsha: processed_commit}
        return None
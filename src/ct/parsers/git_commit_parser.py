# git_commit_parser.py
from typing import Any, Dict, List, Optional
from ct.abstracts import AbstractGitParser
from git import Repo

__All__ = ['GitCommitParser']


class GitCommitParser(AbstractGitParser):
    def parse(self, source: Any, start: Optional[int] = None, end: Optional[int] = None) -> Dict[str, List[str]]:
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
        return [commit_message]

    def get_commit_count(self, source: Any) -> int:
        repo_path = source
        repo = Repo(repo_path)
        return sum(1 for _ in repo.iter_commits())

    def get_commit_by_hash(self, source: Any, hash_prefix: str) -> Optional[Dict[str, List[str]]]:
        repo_path = source
        repo = Repo(repo_path)
        for commit in repo.iter_commits():
            if commit.hexsha.startswith(hash_prefix):
                commit_hash = commit.hexsha
                message = commit.message.strip()
                processed_message = self.process_commit_message(message)
                return {commit_hash: processed_message}
        return None

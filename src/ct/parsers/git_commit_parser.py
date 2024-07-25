from typing import Any, Dict, List
from ct.abstracts import AbstractGitParser
import subprocess
import os
import logging
from git import Repo

__All__ = ['GitCommitParser']


class GitCommitParser(AbstractGitParser):

    def parse(self, source: Any) -> Dict[str, List[str]]:
        commit_messages = {}
        repo_path = source

        #if not os.path.isdir(repo_path):
        #    repo_name = source.split('/')[-1].replace('.git', '')
        #    self.clone_repo(source, repo_name)
        #    repo_path = repo_name

        repo = Repo(repo_path)
        for commit in repo.iter_commits():
            commit_hash = commit.hexsha
            message = commit.message.strip()
            processed_message = self.process_commit_message(message)
            commit_messages[commit_hash] = processed_message

        return commit_messages

    def process_commit_message(self, commit_message: str) -> List[str]:
        # This method can be expanded to process commit messages as needed.
        return [commit_message]

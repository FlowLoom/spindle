from abc import ABC, abstractmethod
from spindle.interfaces import IProcessor, IParser
from typing import Any, Dict, List
import subprocess

__All__ = ["AbstractGitParser"]


class AbstractGitParser(IParser):
    def __init__(self,
                 processor: IProcessor,
                 repo_path: str = None,
                 *args,
                 **kwargs
                 ):
        self.repo_path = repo_path
        self.processor = processor

    def clone_repo(self, repo_url: str, clone_path: str) -> None:
        subprocess.run(['git', 'clone', repo_url, clone_path], check=True)

    @abstractmethod
    def parse(self, source: Any) -> Dict[str, List[str]]:
        pass

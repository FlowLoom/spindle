from spindle.abstracts.abstract_visitor import AbstractVisitor
from spindle.parsers.code_parser import CodeParser
from spindle.parsers.git_commit_parser import GitCommitParser
from spindle.parsers.web_parser import WebParser

__All__ = ['StatisticsVisitor']


class StatisticsVisitor(AbstractVisitor):
    def __init__(self):
        self.stats = {}

    def visit_codeparser(self, parser: CodeParser):
        self.stats['code_files'] = len(parser.parse())

    def visit_gitcommitparser(self, parser: GitCommitParser):
        self.stats['git_commits'] = len(parser.parse())

    def visit_webparser(self, parser: WebParser):
        self.stats['web_content_length'] = len(' '.join(parser.parse().get('web_content', [])))

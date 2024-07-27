from spindle.abstracts.abstract_visitor import AbstractVisitor
from spindle.parsers.code_parser import CodeParser
from spindle.parsers.git_commit_parser import GitCommitParser
from spindle.parsers.web_parser import WebParser

__All__ = ['StatisticsVisitor']


class StatisticsVisitor(AbstractVisitor):
    """
    A visitor class that collects statistics from various parsers.

    This class implements the Visitor pattern to gather statistics from different
    parser types (CodeParser, GitCommitParser, and WebParser).

    Attributes:
        stats (dict): A dictionary to store collected statistics.
    """

    def __init__(self):
        """
        Initialize the StatisticsVisitor with an empty stats dictionary.
        """

        self.stats = {}

    def visit_codeparser(self, parser: CodeParser):
        """
        Visit a CodeParser and collect statistics on the number of code files.

        Args:
            parser (CodeParser): The CodeParser instance to visit.
        """

        self.stats['code_files'] = len(parser.parse())

    def visit_gitcommitparser(self, parser: GitCommitParser):
        """
        Visit a GitCommitParser and collect statistics on the number of git commits.

        Args:
            parser (GitCommitParser): The GitCommitParser instance to visit.
        """

        self.stats['git_commits'] = len(parser.parse())

    def visit_webparser(self, parser: WebParser):
        """
        Visit a WebParser and collect statistics on the total length of web content.

        Args:
            parser (WebParser): The WebParser instance to visit.
        """

        # Calculate the total length of web content by joining all elements
        self.stats['web_content_length'] = len(' '.join(parser.parse().get('web_content', [])))

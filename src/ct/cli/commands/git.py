import click
from ct.cli.commands import cli
from ct.parsers import CodeParser, GitCommitParser
from ct.config import ConfigManager
from ct.handlers import ConsolePrintHandler, FileHandler
from ct.processors import DummyProcessor


__all__ = ["git"]


@cli.command()
@click.option('--repo', required=True, help='Git repository URL or local path')
@click.option('--output', default='output.txt', help='Output file path')
@click.option('--print', '-p', is_flag=True, help='Print output to console instead of writing to file')
def git(repo, output, print):
    """Parse git commit messages and output their content to a text file or console."""



    processor = DummyProcessor()
    parser = GitCommitParser(processor=processor, source=repo)
    parsed = parser.parse(repo)

    if print:
        handler = ConsolePrintHandler()
    else:
        handler = FileHandler(output_file=output)  # Assuming FileHandler is defined for file output

    handler.handle(parsed)

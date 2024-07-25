# git.py
import click
from ct.cli.commands import cli
from ct.parsers import GitCommitParser
from ct.config import ConfigManager
from ct.handlers import ConsolePrintHandler, FileHandler
from ct.processors import DummyProcessor

__all__ = ["git"]


@cli.command()
@click.option('--repo', required=True, help='Git repository URL or local path')
@click.option('--output', default='output.txt', help='Output file path')
@click.option('--print', '-p', is_flag=True, help='Print output to console instead of writing to file')
@click.option('--start', type=int, help='Start index for commit range')
@click.option('--end', type=int, help='End index for commit range')
@click.option('--count', is_flag=True, help='Return the number of commits in the repository')
@click.option('--hash', help='Return commit by full hash or last 5 characters of the hash')
def git(repo, output, print, start, end, count, hash):
    """Parse git commit messages and output their content to a text file or console."""
    processor = DummyProcessor()
    parser = GitCommitParser(processor=processor, source=repo)

    if count:
        commit_count = parser.get_commit_count(repo)
        if print:
            click.echo(f"Total commits: {commit_count}")
        else:
            with open(output, 'w') as f:
                f.write(f"Total commits: {commit_count}\n")
        return

    if hash:
        commit_data = parser.get_commit_by_hash(repo, hash)
        if not commit_data:
            click.echo(f"No commit found with hash: {hash}")
            return
    else:
        commit_data = parser.parse(repo, start, end)

    if print:
        handler = ConsolePrintHandler()
    else:
        handler = FileHandler(output_file=output)
    handler.handle(commit_data)

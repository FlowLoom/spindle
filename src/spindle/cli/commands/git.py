# git.py
import click
from spindle.cli.commands import cli
from spindle.parsers import GitCommitParser
from spindle.config import ConfigManager
from spindle.handlers import ConsolePrintHandler, FileHandler
from spindle.processors import DummyProcessor

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
    """
    Parse git commit messages and output their content to a text file or console.

    Args:
        repo (str): Git repository URL or local path.
        output (str): Output file path. Defaults to 'output.txt'.
        print (bool): Flag to print output to console instead of writing to file.
        start (int, optional): Start index for commit range.
        end (int, optional): End index for commit range.
        count (bool): Flag to return the number of commits in the repository.
        hash (str, optional): Full hash or last 5 characters of the hash to return a specific commit.

    Returns:
        None

    Raises:
        click.ClickException: If there's an error during execution.
    """
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
        #TODO: Currently only supports full hash
        commit_data = parser.get_commit_by_hash(repo, hash)
        if not commit_data:
            click.echo(f"No commit found with hash: {hash}")
            return
    else:
        commit_data = parser.parse(repo, start, end)

    # Choose the appropriate handler based on the print flag
    if print:
        handler = ConsolePrintHandler()
    else:
        handler = FileHandler(output_file=output)
    handler.handle(commit_data)

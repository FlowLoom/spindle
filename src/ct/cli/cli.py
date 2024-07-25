import click
from ct.parsers import CodeParser, GitCommitParser
from ct.config import ConfigManager
from ct.handlers import ConsolePrintHandler, FileHandler
from ct.processors import FileProcessor, DummyProcessor
from ct.cli.commands import code, git, web


__all__ = ["cli"]

@click.group()
def cli():
    """CLI tool for parsing source code files."""
    pass


cli.add_command(code)
cli.add_command(git)
cli.add_command(web)


if __name__ == "__main__":
    cli()

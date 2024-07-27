import click
from spindle.parsers import CodeParser, GitCommitParser
from spindle.config import ConfigManager
from spindle.handlers import ConsolePrintHandler, FileHandler
from spindle.processors import FileProcessor, DummyProcessor
from spindle.cli.commands import code, git, web

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

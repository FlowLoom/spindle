import click
from ct.parsers import CodeParser, GitCommitParser
from ct.config import ConfigManager
from ct.handlers import ConsolePrintHandler, FileHandler
from ct.processors import FileProcessor, DummyProcessor
from ct.cli.commands import code, git


__all__ = ["cli"]

@click.group()
def cli():
    """CLI tool for parsing source code files."""
    pass


cli.add_command(code)
cli.add_command(git)


if __name__ == "__main__":
    cli()

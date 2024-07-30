import click

@click.group()
def cli():
    """CLI tool for parsing source code files."""
    pass


from .code import *
from .git import *
from .web import *
from .fabric import *
from .ticket import *
from .youtube import *
from .save import *

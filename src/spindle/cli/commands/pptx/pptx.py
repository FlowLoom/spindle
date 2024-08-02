import click
from spindle.cli.commands.pptx.get import get

__all__ = ['pptx']


@click.group()
def pptx():
    """Fabric functionality integrated into Spindle."""
    pass


# Add subcommands to the main CLI group
pptx.add_command(get)

import click
from spindle.cli.commands.pptx.get import pptx_get
from spindle.cli.commands.pptx.set.pptx_set import pptx_set

__all__ = ['pptx']


@click.group()
def pptx():
    """Fabric functionality integrated into Spindle."""
    pass


# Add subcommands to the main CLI group
pptx.add_command(pptx_get, name='get')
pptx.add_command(pptx_set, name='set')

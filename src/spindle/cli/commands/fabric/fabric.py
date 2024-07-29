import click
from spindle.cli.commands.fabric.process import process
from spindle.cli.commands.fabric.setup import setup
from spindle.cli.commands.fabric.update import update
from spindle.cli.commands.fabric.gui import gui

__All__ = ['fabric']


@click.group()
def fabric():
    """Fabric functionality integrated into Spindle."""
    pass

# Add subcommands to the main CLI group
fabric.add_command(process)
fabric.add_command(setup)
fabric.add_command(update)
fabric.add_command(gui)

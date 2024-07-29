import click
from spindle.utils.setup import Setup
from spindle.exceptions import SpindleException

__All__ = ['setup']

# TODO: Make setup a root command
# TODO: Move current setup command to a subcommand of init
# TODO: add get and set subcommands to setup to get and set config values
@click.command()
def setup():
    """Set up Fabric configuration."""
    try:
        Setup().run()
    except SpindleException as e:
        click.echo(f"Error during setup: {str(e)}", err=True)
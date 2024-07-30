import click
from spindle.updater import Update
from spindle.utils.alias import Alias
from spindle.exceptions import SpindleException

__All__ = ['update']


@click.command()
def update():
    """Update Fabric patterns."""
    try:
        Update().update_patterns()
        #Alias().execute()
    except SpindleException as e:
        click.echo(f"Error during update: {str(e)}", err=True)

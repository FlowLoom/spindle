import click
from spindle.utils.electron import run_electron_app
from spindle.exceptions import SpindleException

__All__ = ['gui']


@click.command()
def gui():
    """Launch Fabric GUI. (Not implemented)"""
    try:
        run_electron_app()
    except SpindleException as e:
        click.echo(f"Error launching GUI: {str(e)}", err=True)

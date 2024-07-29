import click
from spindle.utils.standalone import Standalone
from spindle.utils.setup import Setup
from spindle.utils.update import Update
from spindle.utils.alias import Alias
from spindle.utils.electron import run_electron_app
from spindle.exceptions import SpindleException

__All__ = ['fabric']

@click.group()
def fabric():
    """Fabric functionality integrated into Spindle."""
    pass

@fabric.command()
@click.option('--text', '-t', help="Text to process with Fabric")
@click.option('--pattern', '-p', help="Fabric pattern to use")
@click.option('--copy', '-C', is_flag=True, help="Copy the response to clipboard")
@click.option('--output', '-o', help="Save the response to a file")
@click.option('--stream', '-s', is_flag=True, help="Stream the response in real-time")
@click.option('--model', '-m', help="Select the model to use")
def process(text, pattern, copy, output, stream, model):
    """Process text using Fabric."""
    try:
        standalone = Standalone(click.get_current_context().params, pattern)
        if not text:
            text = standalone.get_cli_input()

        if stream:
            standalone.stream_message(text)
        else:
            standalone.send_message(text)
    except SpindleException as e:
        click.echo(f"Error: {str(e)}", err=True)

@fabric.command()
def setup():
    """Set up Fabric configuration."""
    try:
        Setup().run()
    except SpindleException as e:
        click.echo(f"Error during setup: {str(e)}", err=True)

@fabric.command()
def update():
    """Update Fabric patterns."""
    try:
        Update().update_patterns()
        Alias().execute()
    except SpindleException as e:
        click.echo(f"Error during update: {str(e)}", err=True)

@fabric.command()
def gui():
    """Launch Fabric GUI."""
    try:
        run_electron_app()
    except SpindleException as e:
        click.echo(f"Error launching GUI: {str(e)}", err=True)

# Add other Fabric-related commands here...
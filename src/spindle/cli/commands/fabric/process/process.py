import sys
import click
from spindle.core import ModelInteractionManager
from spindle.exceptions import SpindleException

__all__ = ["process"]


@click.command()
@click.argument('text', required=False)
#@click.option('--text', '-t', help="Text to process with Fabric")
@click.option('--pattern', '-p', help="Fabric pattern to use")
@click.option('--copy', '-C', is_flag=True, help="Copy the response to clipboard")
@click.option('--output', '-o', help="Save the response to a file")
@click.option('--stream', '-s', is_flag=True, help="Stream the response in real-time")
@click.option('--model', '-m', help="Select the model to use")
def process(text, pattern, copy, output, stream, model):
    """Process text using Fabric."""
    try:
        interaction_manager = ModelInteractionManager(click.get_current_context().params, pattern)

        if not text:
            # TODO: Implement a way to read from stdin in a non-blocking way in interaction_manager
            #  TODO: see if we can do stdin and cli input at the same time
            #text = interaction_manager.get_cli_input()
            text = sys.stdin.read()

        if stream:
            # Handle streaming response
            for chunk in interaction_manager.stream_message(text):
                click.echo(chunk, nl=False)
            click.echo()  # Print a newline at the end of the stream
        else:
            # Handle non-streaming response
            response = interaction_manager.send_message(text)
            click.echo(response)

        # Handle copy and output options
        if copy or output:
            # For streaming, we need to reassemble the full response
            full_response = ''.join(interaction_manager.stream_message(text)) if stream else response

            if copy:
                import pyperclip
                pyperclip.copy(full_response)
                click.echo("Response copied to clipboard.")

            if output:
                with open(output, "w") as f:
                    f.write(full_response)
                click.echo(f"Response saved to {output}")

    except SpindleException as e:
        click.echo(f"Error: {str(e)}", err=True)
    except Exception as e:
        click.echo(f"An unexpected error occurred: {str(e)}", err=True)


if __name__ == '__main__':
    process()

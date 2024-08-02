import click
from spindle.factories import PPTXSetterFetcherFactory
from spindle.cli.commands.pptx.callbacks import parse_slide_index

__all__ = ['pptx_set']


@click.command()
@click.argument('text', type=str)
@click.option('--file', type=click.Path(exists=True), required=True, help='PPTX file path')
@click.option('--slide', callback=parse_slide_index, help='Set content for a specific slide (1-based index)')
@click.option('--notes', is_flag=True, help='Set the content as notes instead of slide content')
@click.option('--output', '-o', type=click.Path(), required=True, help='Output file path')
def pptx_set(file, text, slide, notes, output):
    """Set content or notes for slides in a PPTX file."""
    try:
        factory = PPTXSetterFetcherFactory()

        fetcher = factory.create_fetcher()
        handler = factory.create_handler(output_file=output)

        options = {
            'slide_index': slide,
            'text': text,
            'is_notes': notes
        }

        data = fetcher.fetch(file, **options)
        handler.handle(data)

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

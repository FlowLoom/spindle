import click
from spindle.factories import PPTXFetcherFactory

__all__ = ['pptx']


@click.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--only-content', is_flag=True, help='Extract only slide content')
@click.option('--only-notes', is_flag=True, help='Extract only speaker notes')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
def pptx(file, only_content, only_notes, output):
    """Parse PPTX files and extract content and/or speaker notes."""
    try:
        factory = PPTXFetcherFactory()

        fetcher = factory.create_fetcher()
        handler = factory.create_handler(output_file=output)

        options = {
            'only_content': only_content,
            'only_notes': only_notes,
        }

        data = fetcher.fetch(file, **options)
        handler.handle(data)

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

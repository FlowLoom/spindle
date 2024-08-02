import click
from spindle.factories import PPTXFetcherFactory

__all__ = ['pptx']


def parse_slide_range(ctx, param, value):
    if value is None:
        return None
    try:
        if '-' in value:
            start, end = map(int, value.split('-'))
            if start is end:
                return int(start - 1)

            if start < 1 or end < start:
                raise click.BadParameter('Slide range must start at 1 and be in the format "start-end" where start < end or "start" where start is the slide number.')
            return (start - 1, end)  # Convert to 0-based index
        else:
            slide = int(value)
            return slide - 1  # Convert to 0-based index
    except ValueError:
        raise click.BadParameter('Slide range must be a number or a range (e.g., 1-3). Count starts at 1')

@click.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--only-content', is_flag=True, help='Extract only slide content')
@click.option('--only-notes', is_flag=True, help='Extract only speaker notes')
@click.option('--slide', callback=parse_slide_range, help='Extract specific slide(s) by number or range (e.g., 3 or 1-3)')
@click.option('--only-metadata', is_flag=True, help='Extract only metadata')
@click.option('--no-metadata', is_flag=True, help='Exclude metadata from output')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
def pptx(file, only_content, only_notes, slide, only_metadata, no_metadata, output):
    """Parse PPTX files and extract content, speaker notes, and/or metadata."""
    try:
        factory = PPTXFetcherFactory()

        fetcher = factory.create_fetcher()
        handler = factory.create_handler(output_file=output)

        options = {
            'only_content': only_content,
            'only_notes': only_notes,
            'slide_range': slide,
            'only_metadata': only_metadata,
            'no_metadata': no_metadata
        }

        data = fetcher.fetch(file, **options)
        handler.handle(data)

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


import click
from spindle.factories import YouTubeFetcherFactory
from spindle.config import ConfigManager

__all__ = ['youtube']


@click.command()
@click.argument('url')
@click.option('--duration', '-d', is_flag=True, help='Output only the duration')
@click.option('--transcript', '-t', is_flag=True, help='Output only the transcript')
@click.option('--comments', '-c', is_flag=True, help='Output the comments on the video')
@click.option('--metadata', '-m', is_flag=True, help='Output the video metadata')
@click.option('--lang', '-l', default='en', help='Language for the transcript (default: English)')
@click.option('--output', '-o', help='Output file path')
@click.option('--format', '-f', type=click.Choice(['json', 'plaintext']), default='json', help='Output format')
def youtube(url, duration, transcript, comments, metadata, lang, output, format):
    """Fetch and process YouTube video data."""
    try:
        config = ConfigManager().get_config()
        factory = YouTubeFetcherFactory()

        fetcher = factory.create_fetcher()
        handler = factory.create_handler(output, format)

        options = {
            'duration': duration,
            'transcript': transcript,
            'comments': comments,
            'metadata': metadata,
            'lang': lang
        }

        data = fetcher.fetch(url, options=options)
        handler.handle(data)

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

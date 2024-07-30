import click
from spindle.factories import WebFetcherFactory
from spindle.config import ConfigManager
from spindle.decorators import TimingFetcherDecorator
from spindle.handlers import CompositeHandler
from spindle.exceptions import HandlerException

@click.command()
@click.argument('url', required=False)
#@click.option('--url', required=True, help='URL to scrape text from')
@click.option('--output', help='Output file path')
@click.option('--method', default='traf',
              type=click.Choice(['custom', 'raw', 'traf', 'readability', 'article_parser', 'boilerpy3', 'html2text', 'newspaper', 'goose']),
              help='Content extraction method')
@click.option('--remove-html/--keep-html', default=True, help='Remove HTML tags from the content')
@click.option('--remove-whitespace/--keep-whitespace', default=True, help='Remove excess whitespace')
@click.option('--remove-urls/--keep-urls', default=False, help='Remove URLs from the content')
@click.option('--min-length', type=int, default=0, help='Minimum line length to keep')
@click.option('--max-length', type=int, default=None, help='Maximum line length (truncates longer lines)')
@click.option('--metadata/--no-metadata', default=False, help='Extract and include metadata')
@click.option('--stats', '-s', is_flag=True, help='Print statistics about the web fetcher')
@click.option('--format', type=click.Choice(['json', 'plaintext']), default='plaintext', help='Output format')
@click.option('--color', type=click.Choice(['red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'white']), help='Console output color')
@click.option('--config', help='Path to the configuration file')
def web(url: str, output: str, method: str, remove_html: bool, remove_whitespace: bool, remove_urls: bool,
        min_length: int, max_length: int, metadata: bool, stats: bool, format: str, color: str, config: str):
    """
    Parse web content from a given URL and output the processed content.
    """
    try:
        # Load configuration if a config file is specified
        if config:
            config_manager = ConfigManager(config)
            url = config_manager.get('Web', 'url', fallback=url)
            output = config_manager.get('Web', 'output_file', fallback=output)
            method = config_manager.get('Web', 'extraction_method', fallback=method)
            remove_html = config_manager.getboolean('Web', 'remove_html', fallback=remove_html)
            remove_whitespace = config_manager.getboolean('Web', 'remove_whitespace', fallback=remove_whitespace)
            remove_urls = config_manager.getboolean('Web', 'remove_urls', fallback=remove_urls)
            min_length = config_manager.getint('Web', 'min_length', fallback=min_length)
            max_length = config_manager.getint('Web', 'max_length', fallback=max_length)
            metadata = config_manager.getboolean('Web', 'extract_metadata', fallback=metadata)

        # Create and configure the factory
        factory = WebFetcherFactory()
        factory.set_default_extraction_method(method)
        factory.set_default_remove_html(remove_html)
        factory.set_default_remove_excess_whitespace(remove_whitespace)
        factory.set_default_remove_urls(remove_urls)
        factory.set_default_min_line_length(min_length)
        factory.set_default_max_line_length(max_length)
        factory.set_default_extract_metadata(metadata)

        # Create the fetcher
        fetcher = factory.create_fetcher()
        if stats:
            fetcher = TimingFetcherDecorator(fetcher)

        # Create handlers
        composite_handler = CompositeHandler()
        if output:
            file_handler = factory.create_handler('file', format, output_file=output)
            composite_handler.add_handler(file_handler)
        console_handler = factory.create_handler('console', format, color=color)
        composite_handler.add_handler(console_handler)

        # Fetch and handle the web content
        parsed_data = fetcher.fetch(url)
        composite_handler.handle(parsed_data)

        #click.echo("Web content parsing completed successfully.")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    web()

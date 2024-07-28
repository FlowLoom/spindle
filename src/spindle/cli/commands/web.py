import click
from spindle.factories import WebFetcherFactory
from spindle.config import ConfigManager

@click.command()
@click.option('--url', required=True, help='URL to scrape text from')
@click.option('--output', help='Output file path')
@click.option('--method', default='custom',
              type=click.Choice(['custom', 'raw', 'traf', 'readability', 'article_parser', 'boilerpy3', 'html2text', 'newspaper', 'goose']),
              help='Content extraction method')
@click.option('--remove-html/--keep-html', default=True, help='Remove HTML tags from the content')
@click.option('--remove-whitespace/--keep-whitespace', default=True, help='Remove excess whitespace')
@click.option('--remove-urls/--keep-urls', default=False, help='Remove URLs from the content')
@click.option('--min-length', type=int, default=0, help='Minimum line length to keep')
@click.option('--max-length', type=int, default=None, help='Maximum line length (truncates longer lines)')
@click.option('--metadata/--no-metadata', default=False, help='Extract and include metadata')
@click.option('--console', '-c', is_flag=True, help='Print output to console instead of writing to file')
@click.option('--config', help='Path to the configuration file')
def web(url, output, method, remove_html, remove_whitespace, remove_urls,
        min_length, max_length, metadata, console, config):
    """
    Parse web content from a given URL and output the processed content.
    """
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

    # Create the parser and handler
    fetcher = factory.create_fetcher()
    handler = factory.create_handler(console=console, output=output)

    try:
        # Parse the web content
        parsed_data = fetcher.fetch(url)

        # Handle the parsed data
        handler.handle(parsed_data)

        click.echo("Web content parsing completed successfully.")

        # If metadata was extracted and we're using console output, display it
        if metadata and console:
            if 'metadata' in parsed_data['web_content']:
                click.echo("\nMetadata:")
                for key, value in parsed_data['web_content']['metadata'].items():
                    click.echo(f"{key}: {value}")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

if __name__ == '__main__':
    web()

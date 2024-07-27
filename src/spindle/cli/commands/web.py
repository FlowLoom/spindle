import click
from spindle.cli.commands import cli
from spindle.parsers import WebParser
from spindle.processors import WebProcessor
from spindle.handlers import ConsolePrintHandler, FileHandler

__All__ = ['web']


@cli.command()
@click.option('--url', required=True, help='URL to scrape text from')
@click.option('--output', default='output.txt', help='Output file path')
@click.option('--print', '-p', is_flag=True, help='Print output to console instead of writing to file')
@click.option('--method', default='custom',
              type=click.Choice(['custom', 'raw', 'traf', 'readability', 'article_parser', 'boilerpy3', 'html2text', 'newspaper', 'goose']),
              help='Content extraction method')
def web(url, output, print, method):
    """
    Pull article text from a given URL.

    This function scrapes text content from a specified URL using the chosen extraction method,
    and either prints the result to the console or writes it to a file.

    Args:
        url (str): The URL to scrape text from.
        output (str): The output file path for saving the scraped content.
        print (bool): Flag to indicate whether to print output to console instead of writing to file.
        method (str): The content extraction method to use.

    Returns:
        None

    Raises:
        click.BadParameter: If an invalid URL or extraction method is provided.
    """

    # Initialize the web processor
    processor = WebProcessor()

    # Create a parser with the specified URL and extraction method
    parser = WebParser(processor, url, method=method)

    # Parse the web content
    parsed_data = parser.parse()

    # Select the appropriate handler based on the print flag
    if print:
        handler = ConsolePrintHandler()
    else:
        handler = FileHandler(output_file=output)

    # Handle the parsed data (print to console or write to file)
    handler.handle(parsed_data)

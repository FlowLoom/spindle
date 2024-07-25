import click
from ct.cli.commands import cli
from ct.parsers import WebParser
from ct.processors import WebProcessor
from ct.handlers import ConsolePrintHandler, FileHandler

__All__ = ['web']


@cli.command()
@click.option('--url', required=True, help='URL to scrape text from')
@click.option('--output', default='output.txt', help='Output file path')
@click.option('--print', '-p', is_flag=True, help='Print output to console instead of writing to file')
def web(url, output, print):
    """Pull all text from a given URL."""
    processor = WebProcessor()
    parser = WebParser(processor, url)
    parsed_data = parser.parse()

    if print:
        handler = ConsolePrintHandler()
    else:
        handler = FileHandler(output_file=output)

    handler.handle(parsed_data)
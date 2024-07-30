import click
from spindle.factories import SaveFetcherFactory
from spindle.exceptions import HandlerException

__all__ = ['save']


@click.command()
@click.argument('stub', required=True)
@click.option('-t', '--tag', multiple=True, help="Add additional frontmatter tags")
@click.option('-n', '--nofabric', is_flag=True, help="Don't use the fabric tags, only use tags from --tag")
@click.option('-s', '--silent', is_flag=True, help="Don't output to stdout, only save to the file")
@click.option('-p', '--passthrough', is_flag=True, help="Pass through the input to stdout, even when silent")
def save(stub, tag, nofabric, silent, passthrough):
    """
    A "tee-like" utility to pipeline saving of content, while keeping the output stream intact.
    Can optionally generate "frontmatter" for PKM utilities like Obsidian.
    """
    try:
        factory = SaveFetcherFactory()

        fetcher = factory.create_fetcher()
        handler = factory.create_handler(silent=silent, passthrough=passthrough)

        options = {
            'stub': stub,
            'tags': tag,
            'nofabric': nofabric,
        }

        data = fetcher.fetch(None, **options)
        handler.handle(data)

    except HandlerException as e:
        click.echo(f"Error: {str(e)}", err=True)
    except Exception as e:
        click.echo(f"An unexpected error occurred: {str(e)}", err=True)

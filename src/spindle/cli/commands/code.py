import click
from typing import List
from spindle.factories import CodeFetcherFactory
from spindle.config import ConfigManager
from spindle.decorators import TimingFetcherDecorator
from spindle.handlers import CompositeHandler
from spindle.exceptions import HandlerException

__All__ = ['code']


@click.command()
@click.option('--src', default='./', required=True, help='Source folder path')
@click.option('--output', help='Output file path')
@click.option('--excluded-dirs', default='', help='Comma-separated list of directories to exclude')
@click.option('--excluded-files', default='', help='Comma-separated list of files to exclude')
@click.option('--extensions', default='.py,.js,.html,.css', help='Comma-separated list of file extensions to include')
@click.option('--config', help='Path to the configuration file')
@click.option('--remove-comments', is_flag=True, help='Remove comments from the code')
@click.option('--keep-empty-lines', is_flag=True, help='Keep empty lines in the code')
@click.option('--no-trim', is_flag=True, help='Do not trim whitespace from lines')
@click.option('--stats', '-s', is_flag=True, help='Print statistics about the code fetcher')
@click.option('--format', type=click.Choice(['json', 'plaintext']), default='plaintext', help='Output format')
@click.option('--color', type=click.Choice(['red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'white']), help='Console output color')
def code(src: str, output: str, excluded_dirs: str, excluded_files: str, extensions: str, config: str,
         remove_comments: bool, keep_empty_lines: bool, no_trim: bool, stats: bool, format: str, color: str):
    """
    Parse source code files and output their content to a text file or console.
    """
    try:
        # Load configuration if a config file is specified
        if config:
            config_manager = ConfigManager(config)
            src = config_manager.get('Settings', 'src_folder', fallback=src)
            output = config_manager.get('Settings', 'output_file', fallback=output)
            excluded_dirs = config_manager.get('Exclusions', 'excluded_dirs', fallback=excluded_dirs)
            excluded_files = config_manager.get('Exclusions', 'excluded_files', fallback=excluded_files)
            extensions = config_manager.get('Extensions', 'file_extensions', fallback=extensions)

        # Process input parameters
        excluded_dirs_list = [d.strip() for d in excluded_dirs.split(',') if d.strip()]
        excluded_files_list = [f.strip() for f in excluded_files.split(',') if f.strip()]
        file_extensions_list = [e.strip() for e in extensions.split(',') if e.strip()]

        # Create and configure the factory
        factory = CodeFetcherFactory()
        factory.set_default_excluded_dirs(excluded_dirs_list)
        factory.set_default_excluded_files(excluded_files_list)
        factory.set_default_file_extensions(file_extensions_list)

        # Create the fetcher
        fetcher = factory.create_fetcher(
            remove_comments=remove_comments,
            remove_empty_lines=not keep_empty_lines,
            trim_lines=not no_trim
        )
        if stats:
            fetcher = TimingFetcherDecorator(fetcher)

        # Create handlers
        composite_handler = CompositeHandler()
        if output:
            file_handler = factory.create_handler('file', format, output_file=output)
            composite_handler.add_handler(file_handler)
        console_handler = factory.create_handler('console', format, color=color)
        composite_handler.add_handler(console_handler)

        # Fetch and handle the code
        parsed_data = fetcher.fetch(src)
        composite_handler.handle(parsed_data)

        #click.echo("Code parsing completed successfully.")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    code()
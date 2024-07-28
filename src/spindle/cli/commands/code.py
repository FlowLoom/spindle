# In spindle/cli/commands/code.py

import click
from spindle.factories import CodeParserFactory
from spindle.config import ConfigManager

@click.command()
@click.option('--src', required=True, help='Source folder path')
@click.option('--output', help='Output file path')
@click.option('--excluded-dirs', default='', help='Comma-separated list of directories to exclude')
@click.option('--excluded-files', default='', help='Comma-separated list of files to exclude')
@click.option('--extensions', default='.py,.js,.html,.css', help='Comma-separated list of file extensions to include')
@click.option('--config', help='Path to the configuration file')
@click.option('--remove-comments', is_flag=True, help='Remove comments from the code')
@click.option('--keep-empty-lines', is_flag=True, help='Keep empty lines in the code')
@click.option('--no-trim', is_flag=True, help='Do not trim whitespace from lines')
@click.option('--console', '-c', is_flag=True, help='Print output to console instead of writing to file')
def code(src, output, excluded_dirs, excluded_files, extensions, config,
         remove_comments, keep_empty_lines, no_trim, console):
    """
    Parse source code files and output their content to a text file or console.

    This function serves as the main entry point for the code parsing command. It handles
    configuration loading, input processing, code parsing, and output generation.

    Args:
        src (str): Source folder path to parse.
        output (str): Output file path for parsed content.
        excluded_dirs (str): Comma-separated list of directories to exclude from parsing.
        excluded_files (str): Comma-separated list of files to exclude from parsing.
        extensions (str): Comma-separated list of file extensions to include in parsing.
        config (str): Path to the configuration file.
        remove_comments (bool): Flag to remove comments from the parsed code.
        keep_empty_lines (bool): Flag to keep empty lines in the parsed code.
        no_trim (bool): Flag to prevent trimming whitespace from lines.
        console (bool): Flag to print output to console instead of writing to file.

    Raises:
        click.ClickException: If an error occurs during parsing or handling of parsed data.
    """

    # Load configuration if a config file is specified
    if config:
        config_manager = ConfigManager(config)
        src = config_manager.get('Settings', 'src_folder', fallback=src)
        output = config_manager.get('Settings', 'output_file', fallback=output)
        excluded_dirs = config_manager.get('Exclusions', 'excluded_dirs', fallback=excluded_dirs)
        excluded_files = config_manager.get('Exclusions', 'excluded_files', fallback=excluded_files)
        extensions = config_manager.get('Extensions', 'file_extensions', fallback=extensions)

    # Process input parameters
    excluded_dirs = [d.strip() for d in excluded_dirs.split(',') if d.strip()]
    excluded_files = [f.strip() for f in excluded_files.split(',') if f.strip()]
    file_extensions = [e.strip() for e in extensions.split(',') if e.strip()]

    # Create and configure the factory
    factory = CodeParserFactory()
    factory.set_default_excluded_dirs(excluded_dirs)
    factory.set_default_excluded_files(excluded_files)
    factory.set_default_file_extensions(file_extensions)

    # Create the parser
    parser = factory.create_parser(
        remove_comments=remove_comments,
        remove_empty_lines=not keep_empty_lines,
        trim_lines=not no_trim
    )

    # Parse the source code
    try:
        parsed_data = parser.parse(src)
    except Exception as e:
        click.echo(f"Error parsing source code: {str(e)}", err=True)
        return

    # Create appropriate handler and process the parsed data
    handler = factory.create_handler(console=console, output=output)
    try:
        handler.handle(parsed_data)
    except Exception as e:
        click.echo(f"Error handling parsed data: {str(e)}", err=True)
        return

    #click.echo("Code parsing completed successfully.")

if __name__ == '__main__':
    code()
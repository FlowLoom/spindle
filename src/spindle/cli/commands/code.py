import click
from spindle.cli.commands import cli
from spindle.parsers import CodeParser
from spindle.config import ConfigManager
from spindle.handlers import ConsolePrintHandler, FileHandler
from spindle.processors import FileProcessor
from spindle.visitors import StatisticsVisitor
from spindle.factories import CodeParserFactory
from spindle.decorators import LoggingParserDecorator, TimingParserDecorator

__all__ = ["code"]


@cli.command()
@click.option('--src', required=True, help='Source folder path')
@click.option('--output', help='Output file path')
@click.option('--excluded-dirs', default='', help='Comma-separated list of directories to exclude')
@click.option('--excluded-files', default='', help='Comma-separated list of files to exclude')
@click.option('--extensions', default='.py,.js,.html,.css',
              help='Comma-separated list of file extensions to include')
@click.option('--config', help='Path to the configuration file')
@click.option('--stats', '-s', is_flag=True, help='Print statistics about the parsed files')
def code(src, output, excluded_dirs, excluded_files, extensions, config, stats):
    """
    Parse source code files and output their content to a text file or console.

    This function serves as the main entry point for the code parsing CLI tool. It handles
    configuration management, sets up the parser with specified options, processes the files,
    and optionally gathers statistics.

    Args:
        src (str): Source folder path to parse.
        output (str): Output file path for parsed content.
        excluded_dirs (str): Comma-separated list of directories to exclude from parsing.
        excluded_files (str): Comma-separated list of files to exclude from parsing.
        extensions (str): Comma-separated list of file extensions to include in parsing.
        config (str): Path to the configuration file.
        stats (bool): Flag to indicate whether to print statistics about parsed files.

    Returns:
        None

    Raises:
        click.BadParameter: If invalid parameters are provided.
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

    # Create and configure the parser
    factory = CodeParserFactory()
    parser = factory.create_parser(src, excluded_dirs, excluded_files, file_extensions)

    # Apply decorators for statistics if requested
    if stats:
        parser = LoggingParserDecorator(TimingParserDecorator(parser))

    # Parse the source code
    parsed_data = parser.parse()


    # Create appropriate handler and process the parsed data
    handler = factory.create_handler(output) if output else factory.create_handler()
    handler.handle(parsed_data)

    # Print statistics if requested
    if stats:
        stats_visitor = StatisticsVisitor()
        parser.accept(stats_visitor)
        print("Stats: ", stats_visitor.stats)

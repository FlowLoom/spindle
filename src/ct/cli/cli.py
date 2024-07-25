import click
from ct.parsers import CodeParser
from ct.config import ConfigManager
from ct.handlers import ConsolePrintHandler, FileHandler
from ct.processors import FileProcessor

__all__ = ["cli"]

@click.group()
def cli():
    """CLI tool for parsing source code files."""
    pass

@cli.command()
@click.option('--src', required=True, help='Source folder path')
@click.option('--output', default='output.txt', help='Output file path')
@click.option('--excluded-dirs', default='', help='Comma-separated list of directories to exclude')
@click.option('--excluded-files', default='', help='Comma-separated list of files to exclude')
@click.option('--extensions', default='.py,.js,.html,.css',
              help='Comma-separated list of file extensions to include')
@click.option('--config', help='Path to the configuration file')
@click.option('--print', '-p', is_flag=True, help='Print output to console instead of writing to file')
def code(src, output, excluded_dirs, excluded_files, extensions, config, print):
    """Parse source code files and output their content to a text file or console."""
    if config:
        config_manager = ConfigManager(config)
        src = config_manager.get('Settings', 'src_folder', fallback=src)
        output = config_manager.get('Settings', 'output_file', fallback=output)
        excluded_dirs = config_manager.get('Exclusions', 'excluded_dirs', fallback=excluded_dirs)
        excluded_files = config_manager.get('Exclusions', 'excluded_files', fallback=excluded_files)
        extensions = config_manager.get('Extensions', 'file_extensions', fallback=extensions)

    excluded_dirs = [d.strip() for d in excluded_dirs.split(',') if d.strip()]
    excluded_files = [f.strip() for f in excluded_files.split(',') if f.strip()]
    file_extensions = [e.strip() for e in extensions.split(',') if e.strip()]

    file_processor = FileProcessor()
    parser = CodeParser(file_processor, src, excluded_dirs, excluded_files, file_extensions)
    parsed_files = parser.parse()

    if print:
        handler = ConsolePrintHandler()
    else:
        handler = FileHandler(output_file=output)  # Assuming FileHandler is defined for file output

    handler.handle(parsed_files)

if __name__ == "__main__":
    cli()

import click
from spindle.factories import GitParserFactory
from spindle.config import ConfigManager

@click.command()
@click.option('--repo', required=True, help='Git repository URL or local path')
@click.option('--output', help='Output file path')
@click.option('--start', type=int, help='Start index for commit range')
@click.option('--end', type=int, help='End index for commit range')
@click.option('--count', is_flag=True, help='Return the number of commits in the repository')
@click.option('--hash', help='Return commit by full hash or hash prefix')
@click.option('--extract-ticket', is_flag=True, help='Extract ticket numbers from commit messages')
@click.option('--max-length', type=int, default=72, help='Maximum length of commit messages')
@click.option('--no-capitalize', is_flag=True, help='Do not capitalize the first word of commit messages')
@click.option('--console', '-c', is_flag=True, help='Print output to console instead of writing to file')
@click.option('--config', help='Path to the configuration file')
def git(repo, output, start, end, count, hash, extract_ticket, max_length, no_capitalize, console, config):
    """
    Parse git commit messages and output their content to a text file or console.

    This function serves as the main entry point for the Git commit parsing tool. It handles
    various options for customizing the parsing process and output format.

    Args:
        repo (str): Git repository URL or local path.
        output (str): Output file path for writing parsed commit messages.
        start (int): Start index for commit range.
        end (int): End index for commit range.
        count (bool): Flag to return the number of commits in the repository.
        hash (str): Full hash or hash prefix to return a specific commit.
        extract_ticket (bool): Flag to extract ticket numbers from commit messages.
        max_length (int): Maximum length of commit messages.
        no_capitalize (bool): Flag to not capitalize the first word of commit messages.
        console (bool): Flag to print output to console instead of writing to file.
        config (str): Path to the configuration file.

    Raises:
        click.ClickException: If an error occurs during the parsing or processing of Git commits.
    """

    # Load configuration if a config file is specified
    if config:
        config_manager = ConfigManager(config)
        repo = config_manager.get('Git', 'repo_path', fallback=repo)
        output = config_manager.get('Git', 'output_file', fallback=output)
        extract_ticket = config_manager.getboolean('Git', 'extract_ticket', fallback=extract_ticket)
        max_length = config_manager.getint('Git', 'max_length', fallback=max_length)
        no_capitalize = config_manager.getboolean('Git', 'no_capitalize', fallback=no_capitalize)

    # Create and configure the factory
    factory = GitParserFactory()
    factory.set_default_extract_ticket_number(extract_ticket)
    factory.set_default_max_length(max_length)
    factory.set_default_capitalize_first_word(not no_capitalize)

    # Create the parser
    parser = factory.create_parser()

    try:
        if count:
            # Get and display the total number of commits
            commit_count = parser.get_commit_count(repo)
            click.echo(f"Total commits: {commit_count}")
            return

        if hash:
            # Retrieve a specific commit by hash
            commit_data = parser.get_commit_by_hash(repo, hash)
            if not commit_data:
                click.echo(f"No commit found with hash: {hash}")
                return
        else:
            # Parse commits within the specified range
            commit_data = parser.parse(repo, start, end)

        # Create appropriate handler and process the parsed data
        handler = factory.create_handler(console=console, output=output)
        handler.handle(commit_data)

        click.echo("Git commit parsing completed successfully.")

    except Exception as e:
        # Handle and report any errors that occur during parsing or processing
        click.echo(f"Error: {str(e)}", err=True)

if __name__ == '__main__':
    git()
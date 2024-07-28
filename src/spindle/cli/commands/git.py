import click
from spindle.factories import GitFetcherFactory
from spindle.config import ConfigManager

__All__ = ['git']

@click.command()
@click.option('--repo', default='./', required=True, help='Git repository URL or local path')
@click.option('--output', help='Output file path')
@click.option('--start', type=int, help='Start index for commit range')
@click.option('--end', type=int, help='End index for commit range')
@click.option('--count', is_flag=True, help='Return the number of commits in the repository')
@click.option('--hash', help='Return commit by full hash or hash prefix')
@click.option('--extract-ticket', is_flag=True, help='Extract ticket numbers from commit messages')
@click.option('--max-length', type=int, default=-1, help='Maximum length of commit messages')
@click.option('--no-capitalize', is_flag=True, help='Do not capitalize the first word of commit messages')
@click.option('--stats', '-s', is_flag=True, help='Print statistics about the Git fetcher')
@click.option('--format', type=click.Choice(['json', 'plaintext']), default='plaintext', help='Output format')
@click.option('--color', type=click.Choice(['red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'white']), help='Console output color')
@click.option('--config', help='Path to the configuration file')
def git(repo, output, start, end, count, hash, extract_ticket, max_length, no_capitalize, stats, format, color, config):
    """
    Parse git commit messages and output their content to a text file or console.
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
    factory = GitFetcherFactory()
    factory.set_default_extract_ticket_number(extract_ticket)
    factory.set_default_max_length(max_length)
    factory.set_default_capitalize_first_word(not no_capitalize)

    # Create the fetcher and handler instances
    fetcher = factory.create_fetcher(stats=stats)
    handler = factory.create_handler(output, format, color)

    try:
        if count:
            # Get and display the total number of commits
            commit_count = fetcher.get_commit_count(repo)
            handler.handle({"total_commits": commit_count})
            return

        if hash:
            # Retrieve a specific commit by hash
            commit_data = fetcher.get_commit_by_hash(repo, hash)
            if not commit_data:
                handler.handle({"error": f"No commit found with hash: {hash}"})
                return
        else:
            # Parse commits within the specified range
            commit_data = fetcher.fetch(repo, start, end)

        # Handle the parsed data
        handler.handle(commit_data)

        #click.echo("Git commit parsing completed successfully.")
    except Exception as e:
        # Handle and report any errors that occur during parsing or processing
        handler.handle({"error": str(e)})

if __name__ == '__main__':
    git()
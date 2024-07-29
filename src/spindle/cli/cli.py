import click
from spindle.cli.commands import code, git, web, fabric, ticket

__all__ = ["cli"]


@click.group()
def cli():
    """
    A powerful CLI tool for executing and managing saved automation patterns within the Flowloom ecosystem, enhancing
    precision and efficiency in AI-driven workflows.
    """
    pass


# Add subcommands to the main CLI group
cli.add_command(code)
cli.add_command(git)
cli.add_command(web)
cli.add_command(fabric)
cli.add_command(ticket)

if __name__ == "__main__":
    cli()

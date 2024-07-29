import click
from spindle.cli.commands.ticket.jira.commands import create

__All__ = ["jira"]


@click.group()
def jira():
    """Manage jira tickets."""
    pass

# Add subcommands to the main CLI group
jira.add_command(create)

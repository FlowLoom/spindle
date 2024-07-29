import click
from spindle.cli.commands.ticket.jira import jira

__All__ = ["ticket"]


@click.group()
def ticket():
    """Manage tickets."""
    pass


# Add subcommands to the main CLI group
ticket.add_command(jira)

if __name__ == '__main__':
    ticket()
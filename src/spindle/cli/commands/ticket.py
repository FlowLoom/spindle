import click
import json
from jira import JIRA
from spindle.config import ConfigManager

__All__ = ["ticket"]


@click.group()
def ticket():
    """Manage tickets."""
    pass

@ticket.command()
@click.option('--file', '-f', type=click.Path(exists=True), required=True, help='JSON file containing ticket data')
@click.option('--server', '-s', help='Jira server URL')
@click.option('--username', '-u', help='Jira username')
@click.option('--token', '-t', help='Jira API token')
@click.option('--project', '-P', help='Jira project key')
@click.option('--tags', '-g', multiple=True, help='Tags to add to the tickets')
@click.option('--assignee', '-a', help='ID of the assignee')
@click.option('--close', '-c', is_flag=True, help='Close all created tickets')
def jira(file, server, username, token, project, tags, assignee, close):
    """Create Jira tickets from a JSON file."""
    config_manager = ConfigManager()

    # Load options from the default configuration file if not provided through command-line
    server = server or config_manager.get('JIRA_SERVER', 'server')
    username = username or config_manager.get('JIRA_USERNAME', 'username')
    token = token or config_manager.get('JIRA_TOKEN', 'token')
    project = project or config_manager.get('JIRA_PROJECT', 'project')
    assignee = assignee or config_manager.get('JIRA_ASSIGNEE', 'assignee')

    # Ensure required parameters are provided
    if not all([server, username, token, project]):
        raise click.UsageError("Please provide Jira server, username, token, and project.")

    with open(file) as f:
        ticket_data = json.load(f)

    jira = JIRA(server=server, basic_auth=(username, token))

    for ticket in ticket_data:
        # Format the description with steps
        description = f"{ticket['description']}\n\nSteps:\n"
        for step in ticket['steps']:
            description += f"- {step}\n"

        issue_dict = {
            'project': {'key': project},
            'summary': ticket['title'],
            'description': description,
            'issuetype': {'name': 'Task'},
        }

        # Add tags to the issue dictionary
        if tags:
            issue_dict['labels'] = list(tags)

        # Assign the ticket to the specified user
        if assignee:
            click.echo(f"Assigning ticket to: {assignee}")
            issue_dict['assignee'] = {"id": assignee}

        issue = jira.create_issue(fields=issue_dict)
        click.echo(f"Created ticket: {issue.key} - {issue.fields.summary}")

        # Close the ticket if the --close option is specified
        if close:
            jira.transition_issue(issue, 'Done')
            click.echo(f"Closed ticket: {issue.key} - {issue.fields.summary}")

if __name__ == '__main__':
    ticket()
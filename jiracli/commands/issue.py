import logging
from datetime import datetime

import click
from atlassian import jira

from jiracli.commands.config import instantiate_jira_from_config

#TODO: allow users to decide what datetime format they want to use via config file.
DATETIME_FORMAT = '%m/%d/%y %H:%M'


@click.group(invoke_without_command=True)
@click.argument("company")
@click.argument("ticket")
@click.pass_context
def issue(ctx, company: str, ticket: str):
    """Interact with a ticket; returns ticket info when used without a subcommand.
    \f
    :param ctx: Click context; automatically passed by group.
    :type ctx: click.core.Context
    :param company: Must be one of the companies configured in ``.jira-cli/config``.
    :type company: str
    :param ticket: Issue key, e.g. PROJECT-###.
    :type ticket: str
    """
    jira = instantiate_jira_from_config(company=company)
    ctx.ensure_object(dict)
    ctx.obj['company'] = company
    ctx.obj['ticket'] = ticket
    ctx.obj['jira'] = jira

    if ctx.invoked_subcommand is None:
        get(ctx)


@issue.command()
@click.option("-s", "--started")
@click.option("-c", "--comment")
@click.argument("TIME")
@click.pass_context
def log(ctx, time: str, started: str = None, comment: str = None):
    """Log time into a ticket.
    \f
    :param ctx: Click context; automatically passed by group.
    :type ctx: click.core.Context
    :param time: Amount of time spent, e.g. ``2w 4d 6h 45m``.
    :type time: str
    :param started: Time started at, format ``%m/%d/%y %H:%M``.
    :type started: str
    :param comment: Comment to include in worklog.
    :type comment: str
    """
    worklog = {"timeSpent": time}
    if started:
        started_datetime = datetime.strptime(started, DATETIME_FORMAT)
        worklog["started"] = started_datetime.strftime("%Y-%m-%dT%H:%M:%S.000+0000%z")
    if comment:
        worklog["comment"] = comment
    jira = ctx.obj['jira']
    jira.issue_add_json_worklog(key=ctx.obj['ticket'], worklog=worklog)


def get(ctx):
    """Return information about a ticket.
    \f
    :param ctx: Click context; automatically passed by group.
    :type ctx: click.core.Context
    """
    jira = ctx.obj['jira']
    returned_information = jira.issue(key=ctx.obj['ticket'])
    click.echo()
    click.echo(f"Title:    {returned_information['fields']['summary']}")
    click.echo(f"Reporter: {returned_information['fields']['reporter']['displayName']}")
    click.echo(f"Assignee: {returned_information['fields']['assignee']['displayName']}")
    click.echo(f"Status:   {returned_information['fields']['status']['name']}")
    click.echo(f"URL:      {ctx.obj['jira'].url}/browse/{ctx.obj['ticket']}")
    click.echo()

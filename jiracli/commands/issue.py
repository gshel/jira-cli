import click
import logging
import configparser
from pprint import pprint
import re
import requests
from atlassian import jira

from jiracli.commands.config import instanciate_jira_from_config


MEASURE_IN_SEC = {"w":604800, "d":86400, "h":3600, "m":60}


def get_equivalent_seconds(time_str: str):
    total_seconds = 0
    for i in time_str.split(' '):
        number = int(re.findall("\d+", i)[0])
        measure = re.findall("\D+", i)[0]
        if measure not in MEASURE_IN_SEC.keys():
            raise ValueError(f"Measurement of time must be one of {list(MEASURE_IN_SEC.keys())}; invalid: {measure} in {i}")
        else:
            total_seconds += number * MEASURE_IN_SEC[measure]
    return total_seconds


@click.group()
@click.argument("company")
@click.argument("ticket")
@click.pass_context
def issue(ctx, company: str, ticket: str):
    jira = instanciate_jira_from_config(company=company)
    ctx.ensure_object(dict)
    ctx.obj['company'] = company
    ctx.obj['ticket'] = ticket
    ctx.obj['jira'] = jira

@issue.command()
@click.option("-c", "--comment")
@click.argument("STARTED")
@click.argument("TIME")
@click.pass_context
def log(ctx, started: str, time: str, comment: str):
    """Log time into a ticket."""
    total_seconds = get_equivalent_seconds(time)
    worklog = {
        "started": started,
        "timeSpent": time,
    }
    if comment:
        worklog["comment"] = comment
    jira = ctx.obj['jira']
    # jira.issue_worklog(key=ctx.obj['ticket'], started=started, time_sec=total_seconds, comment=comment)
    response = jira.issue_add_json_worklog(key=ctx.obj['ticket'], worklog=worklog)
    # response = jira.issue_get_worklog(issue_id_or_key=ctx.obj['ticket'])
    pprint(response)
    # logging.info(f"""Logging {time} ({total_seconds}s) into {ctx.obj['company']} {ctx.obj['ticket']} {f"with comment: {comment}" if comment else ""}""")
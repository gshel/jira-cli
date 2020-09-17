import configparser
import logging
import os

import click
from atlassian.jira import Jira

from jiracli import resources


def instantiate_jira_from_config(company: str):
    """Return a Jira instance to interact with.
    \f
    :param company: Name of the company to connect to (from config).
    :type company: str
    """
    uppercase_company = company.upper()
    url = resources.JIRACLI_CONFIGPARSER[uppercase_company]['url']
    username = resources.JIRACLI_CONFIGPARSER[uppercase_company]['username']
    password = resources.JIRACLI_CONFIGPARSER[uppercase_company]['token']
    return Jira(
        url=url.rstrip('/'),
        username=username,
        password=password
    )


@click.group()
def config():
    """Configure connections to multiple Jira instances."""


def init():
    """Create the `.jira-cli` directory and the config file."""
    if not os.path.exists(resources.CONFIG_DIRECTORY):
        logging.debug(f"Not found: {resources.CONFIG_DIRECTORY}")
        os.mkdir(resources.CONFIG_DIRECTORY)  #might need to change to os.makedirs at some point?
        logging.info(f"Created directory: {resources.CONFIG_DIRECTORY}")
    if not os.path.exists(resources.CONFIG_FILEPATH):
        logging.debug(f"Not found: {resources.CONFIG_FILEPATH}")
        open(resources.CONFIG_FILEPATH, "w").write("# This is the jira-cli config file, where information to connect with various Jira instances can be added manually or interactively via the command `jira-cli config add`.\n\n")
        logging.info(f"Created configuration file: {resources.CONFIG_FILEPATH}")


@config.command()
def add():
    """Interactively add a company, its Jira URL, a username, and an API key (preferred) or password to the config."""
    init()
    company = input("COMPANY: ")
    jira_url = input("JIRA URL: ")
    username = input("USERNAME: ")
    associated_api_key = input("API KEY: ")
    resources.JIRACLI_CONFIGPARSER[company.upper()] = {
        'url': jira_url,
        'username': username,
        'token': associated_api_key
    }
    with open(resources.CONFIG_FILEPATH, "a") as config_file:
        resources.JIRACLI_CONFIGPARSER.write(config_file)
    logging.info(f"Added to config: `{company}`")


@config.command()
def validate():
    """Validate the config; if a Jira instance is not publically accessible from the internet, connect to its private network via VPN, then try again."""
    sections = resources.JIRACLI_CONFIGPARSER.sections()
    for company in sections:
        jira = instantiate_jira_from_config(company)
        try:
            jira.get_configurations_of_jira()
            validated = True
        except exceptions.HTTPError:
            logging.debug(exc_info=True)
            validated = False
        click.echo(f"{company}: {validated}")

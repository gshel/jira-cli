import click
import os
import logging
import pathlib
import configparser
from atlassian.jira import Jira
from requests import exceptions


CONFIG_DIRECTORY = os.path.join(pathlib.Path.home(),".jira-cli")
CONFIG_FILEPATH = os.path.join(CONFIG_DIRECTORY, "config")
config_parser = configparser.ConfigParser()
config_parser.read(CONFIG_FILEPATH)


def instanciate_jira_from_config(company: str):
    uppercase_company = company.upper()
    return Jira(
        url=config_parser[uppercase_company]['URL'],
        username=config_parser[uppercase_company]['USERNAME'],
        password=config_parser[uppercase_company]['TOKEN']
    )


@click.group()
def config():
    """Configure connections to multiple Jira instances."""

def init():
    """Create the `.jira-cli` directory and the config file."""
    if not os.path.exists(CONFIG_FILEPATH):
        logging.debug("Configuration file not found.")
        if not os.path.exists(CONFIG_DIRECTORY):
            os.mkdir(CONFIG_DIRECTORY)  #might need to change to os.makedirs at some point?
        open(CONFIG_FILEPATH, "w").write("# This is the jira-cli config file, where information to connect with various Jira instances can be added manually or interactively via the command `jira-cli config add`.\n\n")
        logging.info(f"Created configuration file: `{CONFIG_FILEPATH}`")


@config.command()
def add():
    """Interactively add a company, its Jira URL, your username, and your API key to the config."""
    init()
    company = input("COMPANY: ")
    jira_url = input("JIRA URL: ")
    username = input("USERNAME: ")
    associated_api_key = input("API KEY: ")
    config_parser[company.upper()] = {
        'URL': jira_url,
        'USERNAME': username,
        'TOKEN': associated_api_key
    }
    with open(CONFIG_FILEPATH, "a") as config_file:
        config_parser.write(config_file)
    logging.info(f"Added to config: `{company}`")


@config.command()
def validate():
    """Validate the config; if a Jira instance is not publically accessible from the internet, connect to its private network via VPN, then try again."""
    sections = config_parser.sections()
    for company in sections:
        jira = instanciate_jira_from_config(company)
        try:
            jira.get_configurations_of_jira()
            validated = True
        except exceptions.HTTPError:
            logging.error(exc_info=True)
            validated = False
        click.echo(f"{company}: {validated}")

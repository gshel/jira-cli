import click

from jiracli import _logging
from jiracli.commands import config, issue, version


@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Enable DEBUG level logging.")
@click.option("-vv", "--very-verbose", is_flag=True, help="Enable DEBUG level logging and import library logging.")
def entry_point(verbose: bool, very_verbose: bool):
    _logging.set_verbosity(__name__, verbose, very_verbose)

entry_point.add_command(config.config)
entry_point.add_command(version.version)
entry_point.add_command(issue.issue)

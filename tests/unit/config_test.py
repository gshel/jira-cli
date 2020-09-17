import os
import tempfile
import configparser

import pytest
from unittest.mock import MagicMock, mock_open

from jiracli.commands import config
from jiracli import resources
from jiracli import cli
from click.testing import CliRunner
import logging
import requests

# sanity test to make sure resources.JIRACLI_CONFIGPARSER is configured properly for other tests
@pytest.mark.parametrize("config_key,expected_value", [
    ("url", "https://acme.atlassian.net/"),
    ("username", "sara@acme.com"),
    ("token", "aaabbbccc123456")])
def test_instantiate_jira_from_config__assert_config_values_from_config(golden_config_file, config_key, expected_value):
    assert resources.JIRACLI_CONFIGPARSER["ACME"][config_key] == expected_value


def test_instantiate_jira_from_config__assert_Jira_instantiated(golden_config_file):
    config.Jira = MagicMock()
    config.instantiate_jira_from_config("acme")
    config.Jira.assert_called_with(
        url="https://acme.atlassian.net",
        username="sara@acme.com",
        password="aaabbbccc123456")


def test_init__assert_config_directory_is_not_created(config_directory, empty_config_filepath):
    os.mkdir = MagicMock()
    config.init()
    os.mkdir.assert_not_called()


def test_init__assert_config_filepath_is_not_created(config_directory, empty_config_filepath):
    config.open = mock_open()
    config.init()
    config.open.assert_not_called()


def test_init__assert_config_directory_is_created():
    resources.CONFIG_DIRECTORY = f"{tempfile.gettempdir()}/{tempfile.TemporaryDirectory().name}"
    os.mkdir = MagicMock()
    config.init()
    os.mkdir.assert_called()


def test_init__assert_config_filepath_is_created():
    resources.CONFIG_FILEPATH = tempfile.NamedTemporaryFile(dir=tempfile.gettempdir()).name
    config.open = mock_open()
    config.init()
    config.open.assert_called()


def test_add__assert_init_called(empty_config_filepath, click_runner):
    config.init = MagicMock()
    result = click_runner.invoke(cli.entry_point, ['config', 'add'], input='acme\nhttps://acme.atlassian.net/\nsara@acme.com\naaabbbccc123456')
    config.init.assert_called()


def test_add__assert_generated_file_equals_golden_config(config_directory, empty_config_filepath, click_runner):
    resources.JIRACLI_CONFIGPARSER = configparser.ConfigParser() # must re-initialize here, but no need to read :shrug:
    result = click_runner.invoke(cli.entry_point, ['config', 'add'], input='acme\nhttps://acme.atlassian.net/\nsara@acme.com\naaabbbccc123456')
    populated_config_contents = open(empty_config_filepath).read()
    golden_config_file_contents = open(f"{os.getcwd()}/tests/config.golden").read()
    assert populated_config_contents == golden_config_file_contents
    

# def test_validate__assert(golden_config_file, click_runner):
#     config.instantiate_jira_from_config = MagicMock()
#     config.instantiate_jira_from_config.return_value.get_configurations_of_jira.return_value = requests.exceptions.HTTPError
#     with pytest.raises(requests.exceptions.HTTPError):
#         click_runner.invoke(cli.entry_point, ['config', 'validate'], input='acme')

def test_validate__assert():
    config.instantiate_jira_from_config = MagicMock()
    config.instantiate_jira_from_config.return_value.get_configurations_of_jira.return_value = requests.exceptions.HTTPError
    with pytest.raises(requests.exceptions.HTTPError):
        click_runner.invoke(cli.entry_point, ['config', 'validate'], input='acme')
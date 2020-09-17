import logging
import os
from unittest.mock import MagicMock
import pytest
import tempfile
from click.testing import CliRunner
import shutil
from jiracli import resources
import configparser


RELATIVE_PATH_TO_CONFIG_GOLDEN = f"{os.getcwd()}/tests/config.golden"


@pytest.fixture(scope="session")
def config_directory():
    created_temp_dir = tempfile.TemporaryDirectory(dir=tempfile.gettempdir())
    resources.CONFIG_DIRECTORY = created_temp_dir.name
    os.path.exists(resources.CONFIG_DIRECTORY)
    yield resources.CONFIG_DIRECTORY
    created_temp_dir.cleanup()


@pytest.fixture(scope="session")
def empty_config_filepath(config_directory):
    created_file = tempfile.NamedTemporaryFile(dir=resources.CONFIG_DIRECTORY, delete=False)
    resources.CONFIG_FILEPATH = created_file.name
    logging.debug(resources.CONFIG_FILEPATH)
    logging.debug(os.path.isfile(resources.CONFIG_FILEPATH))
    yield resources.CONFIG_FILEPATH
    created_file.close()


@pytest.fixture(scope="session")
def golden_config_file(config_directory):
    logging.debug(os.getcwd())
    golden_config = shutil.copyfile(RELATIVE_PATH_TO_CONFIG_GOLDEN, f"{resources.CONFIG_DIRECTORY}/config.golden")
    resources.CONFIG_FILEPATH = golden_config
    resources.JIRACLI_CONFIGPARSER = configparser.ConfigParser()
    resources.JIRACLI_CONFIGPARSER.read(golden_config)
    yield resources.CONFIG_FILEPATH, resources.JIRACLI_CONFIGPARSER
    os.remove(golden_config)


@pytest.fixture(scope="session")
def click_runner():
    return CliRunner()    
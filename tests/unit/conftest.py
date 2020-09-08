import logging
import os
from unittest.mock import MagicMock
import pytest
import tempfile
from click.testing import CliRunner
from jiracli import resources


@pytest.fixture(scope="session")
def config_directory():
    resources.CONFIG_DIRECTORY = tempfile.gettempdir()
    yield resources.CONFIG_DIRECTORY


@pytest.fixture(scope="session")
def config_filepath(config_directory):
    created_file = tempfile.NamedTemporaryFile(dir=resources.CONFIG_DIRECTORY)
    resources.CONFIG_FILEPATH = created_file.name
    logging.info(resources.CONFIG_FILEPATH)
    logging.info(os.path.isfile(resources.CONFIG_FILEPATH))
    yield resources.CONFIG_FILEPATH

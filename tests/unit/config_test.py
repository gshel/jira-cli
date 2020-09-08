import os
import tempfile

import pytest
from unittest.mock import MagicMock, mock_open

from jiracli.commands import config
from jiracli import resources


def test_init__assert_config_directory_is_not_created(config_directory, config_filepath):
    os.mkdir = MagicMock()
    config.init()
    os.mkdir.assert_not_called()


def test_init__assert_config_filepath_is_not_created(config_directory, config_filepath):
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


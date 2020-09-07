import os
import pathlib

CONFIG_DIRECTORY = os.path.join(pathlib.Path.home(),".jira-cli")
CONFIG_FILEPATH = os.path.join(CONFIG_DIRECTORY, "config")

#TODO: allow users to decide what datetime format they want to use via config file.
DATETIME_FORMAT = '%m/%d/%y %H:%M'
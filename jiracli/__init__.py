"""
jira-cli
=========
A command-line tool for interacting with multiple Jira instances.
"""

import os
import click


__version__ = open(os.path.join("..", "VERSION")).read().strip()
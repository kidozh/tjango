import functools
from tjango import __version__
import sys
from .color import use_style
import argparse


def show_tjango_version():
    print(
        '-' *
        10 +
        use_style(
            ' Tjango ' +
            __version__ +
            ' ',
            fore='blue') +
        '-' *
        10)


def show_help_info():
    help_str = '''
Available subcommands:

''' + use_style('[Tjango]', fore='yellow') + '''
    startproject

    '''
    print(help_str)


def execute_from_command_line():
    """Run a ManagementUtility."""
    argv = sys.argv[1:]
    show_tjango_version()
    if len(argv) == 0:
        show_help_info()

    print(argv, sys.argv)
    pass

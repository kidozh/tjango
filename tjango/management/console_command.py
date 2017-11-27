import functools
from tjango import __version__
import sys
from .color import use_style
import argparse
import importlib


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
        return

    print(argv, sys.argv)
    module_name = argv[0]
    command_module = importlib.import_module('tjango.management.command.%s'%(module_name),'command')
    print(command_module)
    # execute command
    command_instance = command_module.command()
    command_instance.execute()
    pass

from . import baseCommand
import sys

class command(baseCommand):

    command_text = 'startproject'
    create_type = 'project'
    help_text = 'type <project_name>, <project_name> should be a string and not contradictory with existing package'

    def __init__(self):
        pass

    def execute(self):
        argv = sys.argv[1:]
        if len(argv) == 2:
            project_name = argv[1]
        else:
            raise ValueError('Only one parameters is needed, but you gave %s'%(argv))
        self.create_project_or_app(self.create_type,project_name)
        print('Project %s has been successfully created' %(project_name))
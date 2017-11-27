import shutil
import os
import os.path
import tjango

class DirectoryExistError(Exception):
    pass

class baseCommand(object):

    command_text = ''
    help_text = ''

    def __init__(self):
        pass


    def create_project_or_app(self,create_type,project_or_app_name):
        if create_type not in ['project','app']:
            raise ValueError('%s you input is not supported in creating function'%(create_type))

        current_exe_path = os.getcwd()
        create_project_path = os.path.join(current_exe_path,project_or_app_name)

        # ensure there is no directory
        if os.path.exists(create_project_path):
            raise DirectoryExistError('Project %s you will create exists under %s'%(project_or_app_name,create_project_path))

        # ensure projects or app template path
        tjango_package_path = tjango.__path__[0]
        template_directory_name = '%s_template'%(create_type)
        template_directory_path = os.path.join(tjango_package_path,'conf',template_directory_name)

        shutil.copy(template_directory_path, create_project_path)
        pass
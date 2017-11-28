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
        # print(create_project_path,os.path.exists(create_project_path))

        # ensure there is no directory
        if os.path.exists(create_project_path):
            raise DirectoryExistError('Project %s you will create exists under %s'%(project_or_app_name,create_project_path))

        # ensure projects or app template path
        tjango_package_path = tjango.__path__[0]
        template_directory_name = '%s_template'%(create_type)
        template_directory_path = os.path.join(tjango_package_path,'conf',template_directory_name)
        # copy directory
        shutil.copytree(template_directory_path, create_project_path)
        # render the file
        from tjango.utils.crypto import get_random_string
        render_argv = dict(
            project_name = project_or_app_name,
            app_name = project_or_app_name,
            version = __import__('tjango').get_version(),
            secret_key = get_random_string(length=20)
        )
        # traverse the directory
        import tornado.template
        import tornado.escape

        for file_name in os.listdir(create_project_path):
            # only render file endswith `py-tpl`
            if not file_name.endswith('.py-tpl'):
                continue
            rendering_file_path = os.path.join(create_project_path,file_name)
            with open(rendering_file_path,'r') as rendering_file_handler:
                rendering_file_content = str(rendering_file_handler.read())
                # print(rendering_file_content)
                # using tornado template engine
            template_engine = tornado.template.Template(rendering_file_content,autoescape=None)
            new_file_name = '%s.py'%(file_name.split('.')[0])
            new_file_path = os.path.join(create_project_path,new_file_name)
            with open(new_file_path,'w') as new_file_handler:
                rendered_content = str(template_engine.generate(**render_argv),'utf-8')
                # print(rendered_content)
                new_file_handler.write(rendered_content)
            # remove old template file
            os.remove(rendering_file_path)

        pass
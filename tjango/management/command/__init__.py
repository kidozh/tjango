from tjango.management import BaseCommand,CommandError
from importlib import import_module
import os
from os import path
from tjango.conf import Settings,setting
import tjango

class TemplateCommand(BaseCommand):
    """
    Copy either a Tjango application layout template or a Tjango project
    layout template into the specified directory.
    :param style: A color style object (see django.core.management.color).
    :param app_or_project: The string 'app' or 'project'.
    :param name: The name of the application or project.
    :param directory: The directory to which the template should be copied.
    :param options: The additional variables passed to project or app templates
    """
    # Rewrite the following suffixes when determining the target filename.
    rewrite_template_suffixes = (
        # Allow shipping invalid .py files without byte-compilation.
        ('.py-tpl', '.py'),
    )

    def validate_name(self, name, app_or_project):
        a_or_an = 'an' if app_or_project == 'app' else 'a'
        if name is None:
            raise CommandError('you must provide {an} {app} name'.format(
                an=a_or_an,
                app=app_or_project,
            ))
        # Check it's a valid directory name.
        if not name.isidentifier():
            raise CommandError(
                "'{name}' is not a valid {app} name. Please make sure the "
                "name is a valid identifier.".format(
                    name=name,
                    app=app_or_project,
                )
            )
            # Check it cannot be imported.
        try:
            imp = import_module(name)
        except ImportError:
            print('YES')
            pass
        else:
            print(imp,dir(imp))
            raise CommandError(
                "'{name}' conflicts with the name of an existing Python "
                "module and cannot be used as {an} {app} name. Please try "
                "another name.".format(
                    name=name,
                    an=a_or_an,
                    app=app_or_project,
                )
            )



    def get_file_template_path(self,subdir):
        return path.join(tjango.__path__[0],'conf',subdir)

    def handle(self,app_or_project,name,target=None,**options):
        self.app_or_project = app_or_project

        self.validate_name(name,app_or_project)

        if target is None:
            top_dir = path.join(os.getcwd(),name)
            try:
                os.mkdir(top_dir)
            except FileExistsError:
                raise CommandError("'%s' already exists"%(top_dir))
            except OSError as e:
                raise CommandError(e)

        else:
            top_dir = os.path.abspath(path.expanduser(target))
            if not os.path.exists(top_dir):
                raise CommandError("Destination directory '%s' does not "
                                   "exist, please create it first." % top_dir)

        # Set up setting
        setting_handler = setting()
        if not setting.configured:
            setting_handler.configure()

        # prepared to render files
        subdir = 'project_template' if app_or_project == 'project' else 'app_project'
        file_template_dir = self.get_file_template_path(subdir)
        print('$',file_template_dir)

        prefix_length = len(file_template_dir)+1

        for root,dirs,files in os.walk(file_template_dir):
            path_rest = root[prefix_length:]
            print(path_rest)


if __name__ == '__main__':
    a = TemplateCommand()
    path_name = a.get_file_template_path('project_template')
    a.handle('project','ys')
    # print(path_name)
    # print(len(path_name))
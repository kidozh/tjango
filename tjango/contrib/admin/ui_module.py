import tornado.web
import tornado.escape


class optionModule(tornado.web.UIModule):
    def render(self, option):
        '''
        render option in template
        :param option:
        :return:
        '''
        from tjango.conf.models import configOption
        from tjango.db import database
        flag = False
        try:
            database.connect()
        except BaseException:
            flag = True
            pass
        try:
            if configOption.select().where(configOption.name == option).exists():
                if not flag:
                    database.close()
                return tornado.escape.xhtml_escape(
                    configOption.get(configOption.name == option).value)
            else:
                if not flag:
                    database.close()
                return ''
        except Exception as e:
            return ''




class appModelModule(tornado.web.UIModule):
    def get_template_path(self):
        """Override to customize template path for each handler.

        By default, we use the ``template_path`` application setting.
        Return None to load templates relative to the calling file.
        """
        return None

    def render(self, *args, **kwargs):
        from tjango.contrib.admin.utils import modelFinder
        modelsFinder = modelFinder()
        # a tuple containing three element : app,className,class
        modelsList = modelsFinder.getInstalledModel()
        args = locals()
        args.pop('self')
        return self.render_string(
            'templates/contrib/admin/leftSideBar.html', **args)

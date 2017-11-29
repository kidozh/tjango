# -*- coding: UTF-8 -*-
import tornado.web
import tornado
from tjango.db import connectHandler, database
from tjango.contrib.admin.models import *
import datetime


class baseHandler(tornado.web.RequestHandler):
    def get_template_path(self):
        """Override to customize template path for each handler.

        By default, we use the ``template_path`` application setting.
        Return None to load templates relative to the calling file.
        """
        return None

    # peewee
    def prepare(self):
        try:
            database.connect()
        except BaseException:
            pass
        return super(baseHandler, self).prepare()

    def on_finish(self):
        # save to database...

        if not database.is_closed():
            database.close()
        return super(baseHandler, self).on_finish()

    def get_current_user(self):
        # check current user privilege
        username = self.get_secure_cookie("username")
        # init database connect

        # queryObj = connectInstance.query(adminUser).filter(adminUser.username == username)
        if admin.select().where(admin.username == username).exists():
            # there is a username
            aimUser = admin.select().where(admin.username == username).get()
            if aimUser.isStaff:
                # successfully
                self._current_user = aimUser
                return aimUser

        return None

    def write_error(self, status_code, **kwargs):
        args = locals()
        args.pop('self')
        self.render('error.html', **args)

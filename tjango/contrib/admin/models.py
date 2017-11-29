# -*- coding: UTF-8 -*-
import datetime
import bcrypt
from peewee import *
from tjango.db.models import baseModel
from playhouse.fields import PasswordField


class admin(baseModel):
    username = CharField(unique=True)
    nickname = CharField(max_length=20, null=True)
    password = PasswordField()

    # time
    register_time = DateTimeField(
        default=datetime.datetime.now,
        help_text=u'注册时间')

    # permissions
    isStaff = BooleanField(default=False)
    isAdmin = BooleanField(default=False)

    def authPassword(self, password):
        return self.password.check_password(password)
        # return bcrypt.checkpw(
        #     password.encode('utf-8'),
        #     self.password) and len(password) > 8

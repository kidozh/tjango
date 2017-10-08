from tjango.conf import setting
class connectHandler:
    def __init__(self):
        Setting = setting()
        Setting._setup()
        self.settingMapper = Setting._wrapped
        # configuration from setting
        # get configuration from setting
        # according to peewee we should form that address
        # dialect[+driver]://user:password@host/dbname
        self.DB_HOST = Setting._wrapped.DB_HOST
        self.DB_USER = Setting._wrapped.DB_USER
        self.DB_PASSWD = Setting._wrapped.DB_PASSWD
        self.DB_TYPE = Setting._wrapped.DB_TYPE
        self.DB_DRIVER = Setting._wrapped.DB_DRIVER
        self.DB_NAME = Setting._wrapped.DB_NAME

    @property
    def connect_address(self):
        if self.DB_DRIVER == '':
            # use default driver
            # use default utf8 to prevent encode characters error
            sqlAddress = '%s://%s:%s@%s/%s?charset=utf8' % (
            self.DB_TYPE, self.DB_USER, self.DB_PASSWD, self.DB_HOST, self.DB_NAME)
        else:
            sqlAddress = '%s+%s://%s:%s@%s/%s?charset=utf8' % (
            self.DB_TYPE, self.DB_DRIVER, self.DB_USER, self.DB_PASSWD, self.DB_HOST, self.DB_NAME)
        return sqlAddress




from tjango.db import connectHandler

connectDB = connectHandler()

from playhouse.db_url import connect
database = connect(connectDB.connect_address)


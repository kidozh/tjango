from peewee import *
from tjango.db import database

class baseModel(Model):
    '''
    use for models
    '''
    class Meta:
        '''
        configure for database
        '''
        database = database
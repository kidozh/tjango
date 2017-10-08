from tjango.db.models import baseModel
from peewee import *


class configOption(baseModel):
    '''
    this is option for configuration in template rendering and data rewrite like wp_option
    '''

    name = CharField(100,unique=True)
    value = CharField(100,null=True)

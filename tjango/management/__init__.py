class BaseCommand(object):
    '''
    handle the command
    '''

    def __init__(self):
        pass

    def handle(self,*args,**options):
        raise NotImplementedError('subclass of BaseCommand should provide a handle() method')

class CommandError(Exception):
    pass
__author__ = 'kidozh'
# -*- coding: UTF-8 -*-
from tjango.conf import setting

class modelFinder:
    modelsList = []
    def __init__(self):
        '''
        read configuration then find installed_APP
        :return:
        '''
        Setting = setting()
        Setting._setup()
        # empty this ...
        self.modelsList = []
        self.install_app = Setting._wrapped.INSTALLED_APPS

    def getInstalledModel(self):
        '''
        get all install model
        :return: a list that contains some tuples formatting (name,model)
        '''
        from importlib import import_module
        import inspect
        from tjango.db.models import baseModel
        #

        for app in self.install_app:
            # assembly the model's path
            modelsPath = app + '.models'
            modelsModule = import_module(modelsPath)
            # traverse all models
            appModels = []
            for name,model in inspect.getmembers(modelsModule):
                if inspect.isclass(model) and issubclass(model,baseModel) and model != baseModel:
                    appModels.append((name,model))

            self.modelsList.append((app,appModels))
        return self.modelsList

if __name__ == '__main__':
    import os
    from tjango.conf import ENVIRONMENT_VARIABLE
    # refer the setting modules
    os.environ[ENVIRONMENT_VARIABLE] = 'settings'
    print(os.getcwd())

    finder = modelFinder()
    print(finder.getInstalledModel())

    # create all table
    from tjango.db import database

    database.connect()

    for app,modelList in finder.getInstalledModel():
        print(app,modelList)
        for name,model in modelList:
            print(name)
            try:
                database.create_tables([model])
                print(app+' @ '+ name)
            except Exception as e:
                print(e)
    database.close()
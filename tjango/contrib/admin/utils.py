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
        get all install models
        :return: a list that contains some tuples formatting (name,models)
        '''
        from importlib import import_module
        import inspect
        from tjango.db.models import baseModel

        for app in self.install_app:
            # assembly the models's path
            modelsPath = app + '.models'
            modelsModule = import_module(modelsPath)
            # traverse all models
            appModels = []
            for name, model in inspect.getmembers(modelsModule):
                if inspect.isclass(model) and issubclass(
                        model, baseModel) and model != baseModel:
                    appModels.append((name, model))

            self.modelsList.append((app, appModels))
        return self.modelsList

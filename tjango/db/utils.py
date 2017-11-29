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
        from importlib import import_module
        import inspect
        from tjango.db.models import baseModel
        #

        for app in self.install_app:
            # assembly the models's path
            modelsPath = app + '.models'
            modelsModule = import_module(modelsPath)
            # traverse all models
            appModels = []
            for name,model in inspect.getmembers(modelsModule):
                if inspect.isclass(model) and issubclass(model,baseModel) and model != baseModel:
                    appModels.append((name,model))

            self.modelsList.append((app,appModels))
        return self.modelsList

class fieldFinder:
    def __init__(self):
        pass

    def getAllField(self,appModel):
        '''
        return all the valid field
        :param appModel: a list that containing tuples like (attrname,attr)
        :return:
        '''
        from tjango.db.models import baseModel
        import peewee
        import playhouse

        attrList = []

        # traverse all the attributes
        if issubclass(appModel,baseModel) and appModel !=baseModel:
            for attrName in dir(appModel):
                attr = getattr(appModel,attrName)
                # print appModel, ' > ', attr, type(attr)
                if attr in dir(peewee) or attr in dir(playhouse):
                    # print valid filed in peewee or playhouse module
                    attrList.append((attrName,attr))
            return attrList
        else:
            raise TypeError('%s should be subclass of baseModel' % appModel )
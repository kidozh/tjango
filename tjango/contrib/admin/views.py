# -*- coding: UTF-8 -*-
__author__ = 'kidozh'

import tornado.web
import tornado
import tornado.websocket
import tornado.locale
from tjango.db import connectHandler, database
from tjango.contrib.admin.models import *
import tjango
from tjango.contrib.admin.utils import modelFinder
from tjango.db.utils import fieldFinder
from tornado.web import StaticFileHandler
import os.path
import tornado.locale

# locale
user_locale = tornado.locale.get()

class authBaseHandler(tornado.web.RequestHandler):
    # do not use it in other page since it will reconfigure template

    # compatible with admin static file
    def static_url(self, path, include_host=None, **kwargs):
        if include_host is None:
            include_host = getattr(self, "include_host", False)

        if include_host:
            base = self.request.protocol + "://" + self.request.host
        else:
            base = ""

        return base +'%s'%(self.reverse_url("<class 'tornado.web.StaticFileHandler'>",path))

    def get_template_path(self):
        """Override to customize template path for each handler.

        By default, we use the ``template_path`` application setting.
        Return None to load templates relative to the calling file.
        """
        return None


    def prepare(self):
        # configuration for admin page

        # locale settings
        tornado.locale.load_gettext_translations(os.path.join(tjango.__path__[0],'conf','locale'),'tjango')

        try:
            database.connect()
        except BaseException:
            pass
        return super(authBaseHandler, self).prepare()

    def on_finish(self):
        if not database.is_closed():
            database.close()
        return super(authBaseHandler, self).on_finish()

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
        self.render('templates/contrib/admin/error.html', **args)


class authRequestHandler(authBaseHandler):
    def get(self, *args, **kwargs):
        # self.render('portal/index.html')

        self.render('templates/contrib/admin/login.html')

    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        self.username = username
        self.password = password

        # make sure bcrypt could encrypt this password
        if len(password) < 8 or len(password) >= 21:
            self._reason = '密码应为8-20位'
            self.write_error(500)
        else:
            # auth
            # rewrite by peewee
            # queryObj = connectInstance.query(adminUser).filter(adminUser.username == username)
            # print
            # connectInstance.query(adminUser).filter_by(username=username).count()

            # using peewee
            if admin.select().where(admin.username == username).count():
                # username exist
                aimAdmin = admin.select().where(admin.username == username).get()

                # auth password
                if aimAdmin.authPassword(password):
                    # successfully login
                    self.set_secure_cookie('username', username)
                    # URL configuration
                    from tjango.conf import setting
                    from tjango.conf.urls import urlPackage
                    Setting = setting()
                    Setting._setup()
                    urlMapper = urlPackage(Setting._wrapped.ROOT_URLCONF)
                    # check permission
                    # auth permission

                    if not aimAdmin.isStaff:
                        self._reason = '您的账号目前无法访问仪表盘，请联系管理员。'
                        self.write_error(404)
                    # redirect
                    self.redirect(
                        self.reverse_url('tjango.contrib.admin.views.adminManageHandler'))
                else:
                    self._reason = user_locale.translate('Wrong username or password')
                    self.write_error(404)
            else:
                self._reason = user_locale.translate('Wrong username or password')
                self.write_error(404)

            args = locals()
            args.pop('self')
            # self.render('contrib/admin/login.html', **args)

    def write_error(self, status_code, **kwargs):
        args = locals()
        args.pop('self')
        self.render('templates/contrib/admin/loginError.html', **args)


class adminManageHandler(authBaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        import psutil
        import platform
        # cpu info
        logicalCPU = psutil.cpu_count(logical=True)
        physicsCPU = psutil.cpu_count(logical=False)

        # platform uname
        (system, node, release, version, machine, processor) = platform.uname()

        # cpu usage
        usedCPURate = psutil.cpu_percent(interval=1, percpu=False)

        # memory info
        mem = psutil.virtual_memory()

        # start time
        startTime = psutil.boot_time()

        # network statistics
        network = psutil.net_io_counters(pernic=False)

        from tjango.conf import setting
        Setting = setting()
        Setting._setup()

        logFileExist = getattr(Setting._wrapped, 'LOGFILE', False)

        modelsFinder = modelFinder()
        # a tuple containing three element : app,className,class
        modelsList = modelsFinder.getInstalledModel()

        # fill render parameter
        args = locals()
        args.pop('self')
        self.render('templates/contrib/admin/manage.html', **args)


# a HTTP handler for status api
class statusAPIHandler(authBaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        # import module for neccessary
        import tjango.contrib.admin.system_status
        import tornado.escape

        sysInfo = tjango.contrib.admin.system_status.PsutilStats()
        infoDict = sysInfo.loadSummaryData()
        jsonString = tornado.escape.json_encode(infoDict)
        self.write(jsonString)
        self.finish()


# advanced websocket server
class statusWebsocketAPIHandler(tornado.websocket.WebSocketHandler):
    '''
    this socketHandler is aimed to reduce stress from query system's status
    '''
    clients = []
    cache_size = 200

    # you should change it by yourself
    def check_origin(self, origin):
        return True

    def open(self, *args, **kwargs):
        '''
        make auth then add to client
        :param args:
        :param kwargs:
        :return:
        '''
        import tjango.contrib.admin.system_status
        import tornado.escape

        sysInfo = tjango.contrib.admin.system_status.PsutilStats()
        infoDict = sysInfo.loadSummaryData()
        jsonString = tornado.escape.json_encode(infoDict)
        self.write_message(jsonString)
        # directly get info
        self.clients.append(self)

    def on_message(self, message):

        import tjango.contrib.admin.system_status
        import tornado.escape

        sysInfo = tjango.contrib.admin.system_status.PsutilStats()
        infoDict = sysInfo.loadSummaryData()
        jsonString = tornado.escape.json_encode(infoDict)
        self.write_message(jsonString)

    def on_close(self):
        # msgDict = {'result': 3, 'response-Text': 'GoodBye~', 'response-Time': ''}
        # 0 : connect start
        # 1 : right ,give answer
        # 2 : wrong , give reason
        # 3 : shutdown websocket
        # response Text
        # self.write_message(json.dumps(msgDict))
        for client in self.clients:
            if client == self:
                self.clients.remove(client)
            else:
                pass

    @classmethod
    def update_cache(cls):
        # cls.cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size:]


class appModelManager(authBaseHandler):
    def getModelByName(self, modelName):
        '''
        get models by models's name
        :param modelName: models class
        :return:models class or None object
        '''
        modelFinderInstance = modelFinder()
        packageModels = modelFinderInstance.getInstalledModel()
        # traverse all list then find it

        for package, list in packageModels:
            for name, model in list:
                if name == modelName:
                    return package, model
        return None

    def getValidFieldByModel(self, model):
        '''
        get all valid field in peewee or playhouse
        :param model: models instance which inherit baseModel
        :return: all valid field in peewee or playhouse
        '''
        testFiledFinder = fieldFinder()
        return testFiledFinder.getAllField(model)

    @tornado.web.authenticated
    def get(self, modelName, *args, **kwargs):
        package, aimModel = self.getModelByName(modelName)
        if aimModel is None:
            self._reason = '您所请求的模型不存在或者并未被注册'
            self._status_code = 404
            self.write_error(404)
            return None
        # show this models
        # get all valid field
        allValidField = self.getValidFieldByModel(aimModel)
        allFieldName = [getattr(aimModel, foo)
                        for (foo, instance) in allValidField]
        # set up query
        total_record_cnt = aimModel.select().count()
        query = (aimModel
                 .select(*allFieldName)
                 )
        # for foo in query:
        #    for attrName in [f o for (fo,instance) in allValidField]:
        #        print attrName,getattr(foo,attrName)

        modelsFinder = modelFinder()
        # a tuple containing three element : app,className,class
        modelsList = modelsFinder.getInstalledModel()

        args = locals()
        args.pop('self')
        self.render('templates/contrib/admin/tableData.html', **args)


class appModelAddManager(authBaseHandler):
    def getValidFieldByModel(self, model):
        '''
        get all valid field in peewee or playhouse
        :param model: models instance which inherit baseModel
        :return: all valid field in peewee or playhouse
        '''
        from tjango.db.utils import fieldFinder
        testFiledFinder = fieldFinder()
        return testFiledFinder.getAllField(model)

    def getModelByName(self, modelName):
        '''
        get models by models's name
        :param modelName: models class
        :return:models class or None object
        '''
        modelFinderInstance = modelFinder()
        packageModels = modelFinderInstance.getInstalledModel()
        # traverse all list then find it

        for package, list in packageModels:
            for name, model in list:
                if name == modelName:
                    return package, model
        return None

    def get(self, modelName, *args, **kwargs):
        package, aimModel = self.getModelByName(modelName)
        if aimModel is None:
            self._reason = '您所请求的模型不存在或者并未被注册'
            self._status_code = 404
            self.write_error(404)
            return None

        allValidField = self.getValidFieldByModel(aimModel)
        allFieldName = [getattr(aimModel, fieldName)
                        for (fieldName, field) in allValidField]

        args = locals()
        args.pop('self')
        self.render('templates/contrib/admin/addData.html', **args)

    def post(self, modelName, *args, **kwargs):
        package, aimModel = self.getModelByName(modelName)
        if aimModel is None:
            self._reason = '您所请求的模型不存在或者并未被注册'
            self._status_code = 404
            self.write_error(404)
            return None

        allValidField = self.getValidFieldByModel(aimModel)
        # initialize aimModel
        modelRec = aimModel()
        # traverse all the POST parameters

        try:
            for key in self.request.arguments:
                # print key,self.get_argument(key,None)
                if hasattr(modelRec, key) and self.get_argument(key, 0):
                    # print
                    # key,self.get_argument(key),type(getattr(modelRec,key)) ==
                    # bool
                    if isinstance(
                            getattr(
                                modelRec,
                                key),
                            bool) and self.get_argument(key) == '1':

                        setattr(modelRec, key, True)
                    elif isinstance(getattr(modelRec, key), bool) and self.get_argument(key) == '0':

                        setattr(modelRec, key, False)
                    else:
                        setattr(modelRec, key, self.get_argument(key, 0))
                else:
                    continue
            # save the record
            modelRec.save()
        except Exception as e:
            self._reason = e
            self.write_error(500)
            return
        self.redirect(
            self.reverse_url(
                'tjango.contrib.admin.views.appModelManager',
                modelName))

        args = locals()
        args.pop('self')
        self.render('templates/contrib/admin/addData.html', **args)


class appModelChangeManager(authBaseHandler):
    def getValidFieldByModel(self, model):
        '''
        get all valid field in peewee or playhouse
        :param model: models instance which inherit baseModel
        :return: all valid field in peewee or playhouse
        '''

        testFiledFinder = fieldFinder()
        return testFiledFinder.getAllField(model)

    def getModelByName(self, modelName):
        '''
        get models by models's name
        :param modelName: models class
        :return:models class or None object
        '''
        modelFinderInstance = modelFinder()
        packageModels = modelFinderInstance.getInstalledModel()
        # traverse all list then find it

        for package, list in packageModels:
            for name, model in list:
                if name == modelName:
                    return package, model
        return None

    def getPrimaryKey(self, model):
        import peewee
        fields = self.getValidFieldByModel(model)
        for name, attr in fields:
            if isinstance(attr, peewee.PrimaryKeyField):
                return attr
        return None

    @tornado.web.authenticated
    def get(self, modelName, id, *args, **kwargs):
        # just show result
        package, aimModel = self.getModelByName(modelName)
        if aimModel is None:
            self._reason = '您所请求的模型不存在或者并未被注册'
            self._status_code = 404
            self.write_error(404)
            return None

        allValidField = self.getValidFieldByModel(aimModel)
        primaryKey = self.getPrimaryKey(aimModel)
        aimRow = aimModel.get(primaryKey == id)

        args = locals()
        args.pop('self')
        self.render('templates/contrib/admin/changeData.html', **args)

    @tornado.web.authenticated
    def post(self, modelName, id, *args, **kwargs):
        import peewee
        import playhouse.fields

        package, aimModel = self.getModelByName(modelName)
        if aimModel is None:
            self._reason = '您所请求的模型不存在或者并未被注册'
            self._status_code = 404
            self.write_error(404)
            return None

        allValidField = self.getValidFieldByModel(aimModel)
        primaryKey = self.getPrimaryKey(aimModel)
        aimRow = aimModel.get(primaryKey == id)
        for key in self.request.arguments:
            if hasattr(aimRow, key) and self.get_argument(key, None):

                if isinstance(getattr(aimModel, key), peewee.BooleanField):
                    value = self.get_argument(key)
                    # print value,getattr(aimModel,key)
                    if value == '0':
                        setattr(aimRow, key, False)
                    else:
                        setattr(aimRow, key, True)
                # handle time and datetime please take attention

                else:
                    # for non-password field
                    setattr(aimRow, key, self.get_argument(key, None))
            else:
                continue
        aimRow.save()
        self.redirect(
            self.application.reverse_url(
                'tjango.contrib.admin.views.appModelManager',
                modelName))


class appModelDeleteManager(authBaseHandler):
    def getValidFieldByModel(self, model):
        '''
        get all valid field in peewee or playhouse
        :param model: models instance which inherit baseModel
        :return: all valid field in peewee or playhouse
        '''

        testFiledFinder = fieldFinder()
        return testFiledFinder.getAllField(model)

    def getModelByName(self, modelName):
        '''
        get models by models's name
        :param modelName: models class
        :return:models class or None object
        '''
        modelFinderInstance = modelFinder()
        packageModels = modelFinderInstance.getInstalledModel()
        # traverse all list then find it

        for package, list in packageModels:
            for name, model in list:
                if name == modelName:
                    return package, model
        return None

    def getPrimaryKey(self, model):
        import peewee
        fields = self.getValidFieldByModel(model)
        for name, attr in fields:
            if isinstance(attr, peewee.PrimaryKeyField):
                return attr
        return None

    @tornado.web.authenticated
    def get(self, modelName, id, *args, **kwargs):
        # just show result
        package, aimModel = self.getModelByName(modelName)
        if aimModel is None:
            self._reason = '您所请求的模型不存在或者并未被注册'
            self._status_code = 404
            self.write_error(404)
            return None

        allValidField = self.getValidFieldByModel(aimModel)
        primaryKey = self.getPrimaryKey(aimModel)
        aimRow = aimModel.get(primaryKey == id)

        args = locals()
        args.pop('self')
        self.render('templates/contrib/admin/deleteData.html', **args)

    @tornado.web.authenticated
    def post(self, modelName, id, *args, **kwargs):
        import peewee
        import playhouse.fields

        package, aimModel = self.getModelByName(modelName)
        if aimModel is None:
            self._reason = '您所请求的模型不存在或者并未被注册'
            self._status_code = 404
            self.write_error(404)
            return None

        allValidField = self.getValidFieldByModel(aimModel)
        primaryKey = self.getPrimaryKey(aimModel)
        aimRow = aimModel.get(primaryKey == id)
        # print aimRow.delete_instance()
        aimRow.delete_instance()

        self.redirect(
            self.application.reverse_url(
                'tjango.contrib.admin.view.appModelManager',
                modelName))


class appModelApiManager(authBaseHandler):
    '''
    a api server for dataTables
    '''

    def getModelByName(self, modelName):
        '''
        get models by models's name
        :param modelName: models class
        :return:models class or None object
        '''
        modelFinderInstance = modelFinder()
        packageModels = modelFinderInstance.getInstalledModel()
        # traverse all list then find it

        for package, list in packageModels:
            for name, model in list:
                if name == modelName:
                    return package, model
        return None

    def getValidFieldByModel(self, model):
        '''
        get all valid field in peewee or playhouse
        :param model: models instance which inherit baseModel
        :return: all valid field in peewee or playhouse
        '''
        testFiledFinder = fieldFinder()
        return testFiledFinder.getAllField(model)

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self._reason = 'API目前使用的是dataTable，很抱歉目前您只能使用POST的方法来获得信息。'
        self.write_error(403)

    @tornado.web.authenticated
    def post(self, modelName, *args, **kwargs):
        # get models's name from URL directly
        package, aimModel = self.getModelByName(modelName)
        if aimModel is None:
            self._reason = '您所请求的模型不存在或者并未被注册'
            self._status_code = 404
            self.write_error(404)
            return None
        # show this models
        # get all valid field
        allValidField = self.getValidFieldByModel(aimModel)
        allFieldName = [getattr(aimModel, foo)
                        for (foo, instance) in allValidField]
        # set up query

        # this parameter will be returned directly for ajax query
        draw = self.get_argument('draw')
        start = self.get_argument('start')
        length = self.get_argument('length')

        # read columns configuration from dataTable
        i = 0
        success = True
        # traverse to get value from dataTable configuration
        # first read columns name from dataTable
        columnsInfo = []
        while success:
            # try to get parameters ,if error break right now
            # build up parameters
            parameterData = 'columns[%s][data]' % i
            parameterName = 'columnsCustome[%s][name]' % i
            parameterSearchable = 'columns[%s][searchable]' % i
            parameterOrderable = 'columns[%s][orderable]' % i
            parameterSearchVal = 'columns[%s][search][value]' % i
            parameterSearchRegex = 'columns[%s][search][regex]' % i

            try:
                # then search it
                data = self.get_argument(parameterData)
                name = self.get_argument(parameterName)
                searchable = self.get_argument(parameterSearchable)
                orderable = self.get_argument(parameterOrderable)
                searchval = self.get_argument(parameterSearchVal)
                searchRegex = self.get_argument(parameterSearchRegex)
                columnsInfo.append(
                    (data, name, searchable, orderable, searchval, searchRegex))
            except Exception as e:
                success = False
            finally:
                i += 1

        # then get order information
        orderInfo = []
        i = 0
        success = True
        while success:
            # build up order information parameters
            parameterOrderColumn = 'order[%s][column]' % i
            parameterOrderDir = 'order[%s][dir]' % i
            try:
                orderColumn = self.get_argument(parameterOrderColumn)
                orderDir = self.get_argument(parameterOrderDir)
                orderInfo.append((orderColumn, orderDir))
            except BaseException:
                success = False
            finally:
                i += 1

        # build up query
        # get needed paramter from Database

        allNeededField = [
            getattr(
                aimModel,
                name) for (
                data,
                name,
                searchable,
                orderable,
                searchVal,
                searchRegex) in columnsInfo]
        # get orderable info from parameter
        orderField = []

        for (orderCol, orderDir) in orderInfo:

            orderCol = int(orderCol)
            aimOrder = getattr(aimModel, columnsInfo[orderCol][1])
            # check whether this columns are orderable
            if columnsInfo[orderCol][3] == False:
                break
            if orderDir == 'desc':
                orderField.append(aimOrder.desc())
            else:
                orderField.append(aimOrder)
        # get paramter from where
        # assembly query
        recordsTotal = aimModel.select().count()
        start = int(start)
        length = int(length)
        if length > recordsTotal - start:
            length = recordsTotal - start
        searchVal = self.get_argument('search[value]')

        # print '#',searchval,self.get_argument('search[value]')

        if searchVal:
            # find the searchable columns
            # print '# search Value : ',searchVal

            searchRequirement = [
                getattr(
                    aimModel,
                    name).contains(searchVal) for (
                    data,
                    name,
                    searchable,
                    orderable,
                    i,
                    searchRegex) in columnsInfo if searchable and (
                    isinstance(
                        getattr(
                            aimModel,
                            name),
                        TextField) or isinstance(
                        getattr(
                            aimModel,
                            name),
                        CharField))]
            # !!!! default is using OR operator !!!!
            # print '# ',searchRequirement
            if len(searchRequirement) > 0:
                limit = searchRequirement[0]
                for eachLimit in searchRequirement[1:]:
                    limit = limit | eachLimit
                # print
                # len(aimModel.select(*allNeededField).where(getattr(aimModel,'codeA').contains('%s'%(searchVal))))
                query = aimModel.select(
                    *
                    allNeededField).order_by(
                    *
                    orderField).where(limit)[
                    start:start +
                    length]
                recordsFiltered = aimModel.select(
                    *
                    allNeededField).order_by(
                    *
                    orderField).where(limit).count()
            else:
                query = aimModel.select(
                    *
                    allNeededField).order_by(
                    *
                    orderField)[
                    start:start +
                    length]
                recordsFiltered = aimModel.select(
                    *
                    allNeededField).order_by(
                    *
                    orderField).count()
        else:
            query = aimModel.select(
                *
                allNeededField).order_by(
                *
                orderField)[
                start:start +
                length]
            recordsFiltered = aimModel.select(
                *
                allNeededField).order_by(
                *
                orderField).count()
        # assembly the result

        # recordsFiltered = len(query)
        data = []
        import datetime
        import tornado.locale
        import time

        for row in query:
            listData = []
            dataDict = {}
            for index in range(len(columnsInfo)):
                name = columnsInfo[index][1]
                obj = getattr(row, name)
                if isinstance(obj, datetime.datetime):
                    # obj = time.mktime(obj.timetuple())
                    obj = obj.strftime("%Y-%m-%d %H:%M:%S")
                elif (isinstance(obj, str)):
                    # only add 100
                    if len(obj) > 100:
                        obj = '%s...' % (obj[0:99])
                elif isinstance(obj,bytes):
                    obj = obj.decode('utf-8')
                dataDict[name] = obj
                listData.append(obj)
            data.append(listData)

        # retrevie data from local variables
        returnedData = {}
        returnedData['draw'] = draw
        returnedData['recordsTotal'] = recordsTotal
        returnedData['recordsFiltered'] = recordsFiltered
        returnedData['data'] = data
        print(data)

        import tornado.escape
        # self.write(json.dumps(returnedData))
        self.write(tornado.escape.json_encode(returnedData))
        self.finish()

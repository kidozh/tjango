import tjango.contrib.admin.ui_module
import tornado.web
import os.path
import tjango

urlpatterns = [
    ('/', 'tjango.contrib.admin.views.adminManageHandler'),
    ('/login/', 'tjango.contrib.admin.views.authRequestHandler'),
    ('/manage/', 'tjango.contrib.admin.views.adminManageHandler'),
    ('/manage/(?P<modelName>.+)/data/', 'tjango.contrib.admin.views.appModelApiManager'),
    ('/manage/(?P<modelName>.+)/show/', 'tjango.contrib.admin.views.appModelManager'),
    ('/manage/(?P<modelName>.+)/add/', 'tjango.contrib.admin.views.appModelAddManager'),
    ('/manage/(?P<modelName>.+)/change/(?P<id>.+)/',
     'tjango.contrib.admin.views.appModelChangeManager'),
    ('/manage/(?P<modelName>.+)/delete/(?P<id>.+)/',
     'tjango.contrib.admin.views.appModelDeleteManager'),
    # monitor system
    ('/serverStatus', 'tjango.contrib.admin.views.statusAPIHandler'),
    ('/serverStatusWS', 'tjango.contrib.admin.views.statusWebsocketAPIHandler'),
    # chat channel so that administrator could chat realtime or record some
    # data
    # static admin file
    ('/static/admin/(.*?)',tornado.web.StaticFileHandler,dict(path=os.path.join(tjango.__path__[0],'contrib','admin','static')))

]

UImodule = {
    'get_option': tjango.contrib.admin.ui_module.optionModule,
    'adminlte_load_left_sidebar': tjango.contrib.admin.ui_module.appModelModule
}


# cron should be (func,every ms)

cron = [

]

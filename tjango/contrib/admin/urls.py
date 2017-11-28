import tjango.contrib.admin.ui_module

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

]

UImodule = {
    'get_option': tjango.contrib.admin.ui_module.optionModule,
    'adminlte_load_left_sidebar': tjango.contrib.admin.ui_module.appModelModule
}


# cron should be (func,every ms)

cron = [

]

import tjango.contrib.admin.ui_module

urlpatterns = [
    ('/', 'contrib.admin.view.adminManageHandler'),
    ('/login/', 'contrib.admin.view.authRequestHandler'),
    ('/manage/', 'contrib.admin.view.adminManageHandler'),
    ('/manage/(?P<modelName>.+)/data/', 'contrib.admin.view.appModelApiManager'),
    ('/manage/(?P<modelName>.+)/show/', 'contrib.admin.view.appModelManager'),
    ('/manage/(?P<modelName>.+)/add/', 'contrib.admin.view.appModelAddManager'),
    ('/manage/(?P<modelName>.+)/change/(?P<id>.+)/',
     'contrib.admin.view.appModelChangeManager'),
    ('/manage/(?P<modelName>.+)/delete/(?P<id>.+)/',
     'contrib.admin.view.appModelDeleteManager'),
    # monitor system
    ('/serverStatus', 'contrib.admin.view.statusAPIHandler'),
    ('/serverStatusWS', 'contrib.admin.view.statusWebsocketAPIHandler'),
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

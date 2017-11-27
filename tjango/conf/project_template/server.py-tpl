import tornado.web
import os

# import URL manually
from tjango.conf.urls import urlPackage,templateModuleFinder,periodTaskFinder
import tornado
from tornado.options import options,define
# define the port in order to simplify debug mode

define("port", default=8000, help="run on the given port", type=int)
if __name__ == "__main__":

    # set environmental value for setting
    from tjango.conf import ENVIRONMENT_VARIABLE,setting
    # refer the setting modules
    os.environ[ENVIRONMENT_VARIABLE] = 'setting'

    # parse command
    tornado.options.parse_command_line()

    # for URL configuration
    Setting = setting()
    Setting._setup()
    urlMapper = urlPackage(Setting._wrapped.ROOT_URLCONF)

    # for module configuration
    moduleFinder = templateModuleFinder()

    # create table and database
    # empty for extension


    # --------------------------------------------------
    #
    # for log configuration
    #
    # --------------------------------------------------
    if hasattr(Setting._wrapped, "LOGFILE") and Setting._wrapped.LOGFILE:
        import logging
        import yaml
        import logging.config
        from logging import StreamHandler
        from logging.handlers import RotatingFileHandler,SMTPHandler,TimedRotatingFileHandler

        logFilePath = Setting._wrapped.LOGFILE
        logging.config.dictConfig(yaml.load(open('logging.yaml', 'r')))

    # -------------------------------------------
    #
    # end log module
    #
    # -------------------------------------------

    # setting
    settings = {
        "xsrf_cookies": True,
        "login_url": Setting._wrapped.LOGIN_URL,
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret": Setting._wrapped.SECRET_KEY,
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "debug": Setting._wrapped.DEBUG,
    }

    app = tornado.web.Application(
        # get Exported URL
        handlers = urlMapper.detectURL(),
        # get Export UI modules
        ui_modules=moduleFinder.uiDict,
        **settings
    )

    http_server = tornado.httpserver.HTTPServer(app,xheaders = True)
    http_server.listen(options.port)
    # import prase log

    # gather all cron
    cronFinder = periodTaskFinder()
    for (func,ms) in cronFinder.periodTask:
        print('[CRON] %s will recycle in every %s ' %(func,ms))
        tornado.ioloop.PeriodicCallback(func,ms).start()
    print('[CRON] all task is listed...')
    tornado.ioloop.IOLoop.instance().start()
__author__ = 'kidozh'
# -*- coding: UTF-8 -*-

from importlib import import_module
from tjango.exception import ImproperlyConfigured
from tjango.conf import setting


class urlPackage:
    """
    store the URL
    """
    pattern = []
    # this is the map from handler to URL
    URLMapper = {}

    def __init__(self, url_module):
        # check whether this file is properly configured
        if isinstance(url_module, str):
            # url_module is string , just import it
            urlconf_module = import_module(url_module)
        else:
            urlconf_module = url_module
        patterns = getattr(urlconf_module, 'urlpatterns', [])
        # get this
        if isinstance(patterns, list):
            self.patterns = patterns
        else:
            raise ImproperlyConfigured(
                'url_module should contain a list-typed urlpattern variable'
            )

    def detectURL(self, headURL='', itertime=0):
        """
        get url
        :headURL :the former URL which need to be merged
        :return: (url,url_module)
        """
        from tornado.web import URLSpec
        urlList = []
        # print urlList
        for it in self.patterns:
            if isinstance(it, URLSpec):
                urlList.append(it)
                continue
            else:
                # compatible with native tornado url configuration
                url, url_module = it[:2]
                if len(it) > 2:
                    # there maybe some other configuration setting
                    other_config = it[2:]
                else:
                    other_config = []

            # iterable get the URL
            if isinstance(url_module, urlPackage):
                # BFS get URL then extend it
                urlList.extend(
                    url_module.detectURL(
                        headURL='%s%s' %
                        (headURL, url), itertime=itertime + 1))
            elif isinstance(url_module, str):
                # print url_module
                # for individual one then add it to the list
                if headURL:
                    assemblyURL = '%s%s' % (headURL, url)
                else:
                    assemblyURL = '%s' % url
                    # convert it to URLSpec
                urlList.append(
                    URLSpec(
                        assemblyURL,
                        url_module,
                        *other_config,
                        name=url_module))
                # set up mapper for
                self.URLMapper[url_module] = assemblyURL
            else:
                # try to use directly
                if headURL:
                    assemblyURL = '%s%s' % (headURL, url)
                else:
                    assemblyURL = '%s' % url
                urlList.append(
                    URLSpec(
                        assemblyURL,
                        url_module,
                        *other_config
                        ,name=str(url_module)
                    )
                )
                # raise ImproperlyConfigured(
                #     'URL only accept string or URLpackage object(you can use include)'
                # )
        return urlList


def include(urlModules):
    """
    include modules then return all of their package
    """
    # get pattern from configured file

    # for configure
    return urlPackage(urlModules)


class templateModuleFinder:
    def __init__(self):
        '''
        init conf object and get searched path
        :return:
        '''
        # get conf object
        Setting = setting()
        Setting._setup()
        self.searchApp = getattr(Setting._wrapped, 'INSTALLED_APPS')

    @property
    def uiDict(self):
        if not self.searchApp:
            # return a null dict
            return {}
        else:
            returnedDict = {}
            for app in self.searchApp:
                appUrlPath = '%s.urls' % (app)
                appUrlConf = import_module(appUrlPath)
                appUIDict = getattr(appUrlConf, 'UImodule', {})
                # traverse dict and try to import it
                if isinstance(appUIDict, dict):
                    # merge dict
                    returnedDict.update(appUIDict)
                else:
                    raise ImproperlyConfigured(
                        'UImodule in %s should be configured in dict way' % (app))
            return returnedDict


class periodTaskFinder:
    def __init__(self):
        '''
        init conf object and get searched path
        :return:
        '''
        # get conf object

        Setting = setting()
        Setting._setup()
        self.searchApp = getattr(Setting._wrapped, 'INSTALLED_APPS')

    @property
    def periodTask(self):
        '''
        generate a task recursively
        :return:
        '''
        if not self.searchApp:
            # return a null dict
            return None
        else:

            returnedList = []
            for app in self.searchApp:
                appUrlPath = '%s.urls' % (app)
                appUrlConf = import_module(appUrlPath)
                appUIDict = getattr(appUrlConf, 'cron', [])
                # traverse dict and try to import it
                if isinstance(appUIDict, list):
                    # merge dict
                    returnedList.extend(appUIDict)
                else:
                    raise ImproperlyConfigured(
                        'UImodule in %s should be configured in dict way' % (app))
            return returnedList

# -*- coding: UTF-8 -*-
__author__ = 'kidozh'
"""
Default tjango settings. Override these with settings in the module pointed to
by the TJANGO_SETTINGS_MODULE environment variable.
"""

####################
# CORE             #
####################


DEBUG = False

# People who get code error notifications.
# In the format [('Full Name', 'email@example.com'), ('Full Name',
# 'anotheremail@example.com')]
ADMINS = []

# Hosts/domain names that are valid for this site.
# "*" matches anything, ".example.com" matches example.com and all subdomains
ALLOWED_HOSTS = []

# Local time zone for this installation. All choices can be found here:
# https://en.wikipedia.org/wiki/List_of_tz_zones_by_name (although not all
# systems may support all possibilities). When USE_TZ is True, this is
# interpreted as the default user time zone.
TIME_ZONE = 'Asia/Shanghai'

# If you set this to True, Tjango will use timezone-aware datetimes.
USE_TZ = False

# Host for sending email.
EMAIL_HOST = 'localhost'

# Port for sending email.
EMAIL_PORT = 25

# Whether to send SMTP 'Date' header in the local time zone or in UTC.
EMAIL_USE_LOCALTIME = False

# A secret key for this particular Django installation. Used in secret-key
# hashing algorithms. Set this in your settings, or Tjango will complain
# loudly.
SECRET_KEY = ''

# Optional SMTP authentication information for EMAIL_HOST.
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
EMAIL_SSL_CERTFILE = None
EMAIL_SSL_KEYFILE = None
EMAIL_TIMEOUT = None

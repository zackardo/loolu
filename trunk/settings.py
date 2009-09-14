"""
LooLu is Copyright (c) 2009 Shannon Johnson, http://loo.lu/

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os, sys

from ragendja.settings_pre import *

SITE_ID = 1

# Increase this when you update your media on the production site, so users
# don't have to refresh their cache. By setting this your MEDIA_URL
# automatically becomes /media/MEDIA_VERSION/
MEDIA_VERSION = 1


# Make this unique, and don't share it with anybody.
SECRET_KEY = '1234567890'

if on_production_server:
    DEFAULT_FROM_EMAIL = 'bla@bla.com'
    SERVER_EMAIL = DEFAULT_FROM_EMAIL
    MEDIA_URL = 'http://static.loo.lu/media/%d/'
else:
    DEBUG = 1
    MEDIA_URL = '/%d/'
    #ENABLE_PROFILER = True
    #ONLY_FORCED_PROFILE = True
    #PROFILE_PERCENTAGE = 25
    #SORT_PROFILE_RESULTS_BY = 'cumulative' # default is 'time'
    #PROFILE_PATTERN = 'ext.db..+\((?:get|get_by_key_name|fetch|count|put)\)'

# Enable I18N and set default language to 'en'
USE_I18N = True
LANGUAGE_CODE = 'en'

# Restrict supported languages (and JS media generation)
LANGUAGES = (
    ('en', 'English'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.media',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'common.middleware.LogRequestMiddleware',
)

GLOBALTAGS = (

)

SESSION_ENGINE      = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE  = 5*(365*24*60*60) # 5 Years 
SESSION_COOKIE_NAME = '_sess'

LOGIN_URL = '/account/login/'
LOGOUT_URL = '/account/logout/'
LOGIN_REDIRECT_URL = '/'

INSTALLED_APPS = (
    'django.contrib.sessions',
    'django.contrib.admin',
    'loolu',
    'jquery',
    'mediautils',
)

# List apps which should be left out from app settings and urlsauto loading
IGNORE_APP_SETTINGS = IGNORE_APP_URLSAUTO = (

)

MAX_URL_LEN          = 500 
MAX_DESCRIPTION_LEN  = 100
MAX_CUSTOM_NAME_LEN  = 10
MAX_PRIVACY_CODE_LEN = 10

SPIDER_ENABLED       = True
SPIDER_IN_BACKGROUND = False

DEFAULT_SUBDOMAIN='go'

SUBDOMAINS = [
    'i',
    'go',
    'art',
    'biz',
    'news',
    'tech',
    'sports',
    'pic',
    'vid',
]


from ragendja.settings_post import *


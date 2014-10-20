# -*- coding: UTF-8 -*-
# Copyright 2002-2014 by Luc Saffre.
# License: BSD, see LICENSE for more details.

#~ from __future__ import unicode_literals

import os
import sys

from os.path import join, abspath, dirname, normpath, isdir

execfile(join(dirname(__file__), 'project_info.py'))
__version__ = SETUP_INFO['version']
intersphinx_urls = dict(docs="http://site.lino-framework.org")
srcref_url = 'https://github.com/lsaffre/djangosite/blob/master/%s'


from django import VERSION

if VERSION[0] == 1:
    if VERSION[1] > 6:
        AFTER17 = True
    else:
        AFTER17 = False
else:
    raise Exception("Unsupported Django version %s" % VERSION)


__copyright__ = "Copyright (c) 2002-2014 Luc Saffre."

DJANGO_DEFAULT_LANGUAGE = 'en-us'


def assert_django_code(django_code):
    if '_' in django_code:
        raise Exception("Invalid language code %r. "
                        "Use values like 'en' or 'en-us'." % django_code)


def startup():
    from django.conf import settings
    if False:
        settings.SITE.startup()
    else:
        try:
            settings.SITE.startup()
        except ImportError as e:
            import traceback
            #~ traceback.print_exc(e)
            #~ sys.exit(-1)
            raise Exception("ImportError during startup:\n" +
                            traceback.format_exc(e))


if AFTER17:

    from django.apps import AppConfig

    class AppConfig(AppConfig):
        name = 'djangosite'
        # verbose_name = "Djangosite"
    
        def ready(self):
            
            startup()

    default_app_config = 'djangosite.AppConfig'


from .djangosite_site import *


__all__ = ['Site']

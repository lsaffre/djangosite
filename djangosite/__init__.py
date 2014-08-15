# -*- coding: UTF-8 -*-
# Copyright 2002-2013 by Luc Saffre.
# License: BSD, see LICENSE for more details.

#~ from __future__ import unicode_literals

import os
import sys

from os.path import join, abspath, dirname, normpath, isdir

execfile(join(dirname(__file__), 'project_info.py'))
__version__ = SETUP_INFO['version']
intersphinx_url = "http://site.lino-framework.org"
srcref_url = 'https://github.com/lsaffre/djangosite/blob/master/%s'

#~ __author__ = "Luc Saffre <luc.saffre@gmx.net>"

#~ __url__ = "http://lino.saffre-rumma.net"
#~ __url__ = "http://code.google.com/p/lino/"
#~ __url__ = "http://www.lino-framework.org"


__copyright__ = "Copyright (c) 2002-2014 Luc Saffre."

DJANGO_DEFAULT_LANGUAGE = 'en-us'


def assert_django_code(django_code):
    if '_' in django_code:
        raise Exception("Invalid language code %r. "
                        "Use values like 'en' or 'en-us'." % django_code)

from .djangosite_site import *


__all__ = ['Site']

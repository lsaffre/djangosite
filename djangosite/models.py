# -*- coding: UTF-8 -*-
"""
This module is based on Ross McFarland idea to simply send 
the server startup signal "at the end of your last app's models.py file"
in his post `Django Startup Signal (Sun 24 June 2012)
<http://www.xormedia.com/django-startup-signal/>`_.

This adds a subtle hack to also cope with postponed imports.
If there are postponed apps, then :mod:`djangosite.models` must itself raise 
an `ImportError` so that it gets itself postponed and imported another 
time.

Note that `loading.cache.postponed` 
contains all postponed imports even if they succeeded 
at the second attempt.

:copyright: Copyright 2013 by Luc Saffre.
:license: BSD, see LICENSE for more details.
"""

import sys
from django.db.models import loading

if len(loading.cache.postponed) > 0:
    if not 'djangosite' in loading.cache.postponed: # i.e. if this is the first time
        raise ImportError("Waiting for postponed apps (%s) to import" % 
            loading.cache.postponed)

from django.conf import settings
try:
    settings.SITE.startup()
except ImportError as e:
    import traceback
    #~ traceback.print_exc(e)
    #~ sys.exit(-1)
    raise Exception("ImportError during startup: \n" + traceback.format_exc(e))

"""
Usage:

Create a file :file:`/etc/atelier/config.py` with something 
like this::

    from atelier.djangoconf import register_env

    VIRTUALENV_ROOT = '/usr/local/pythonenv'
    DEFAULT_PYTHON_VERSION = '2.6'
    LOCAL_PYTHONPATH = '/home/luc/mypy'
    DEBUG=False

    register_env('demo','2.6')
    register_env('prod','2.6')
    register_env('test','2.6')


Then for each Django project on your host you can use the 
same files :file:`manage.py` and :file:`wsgi.py`::

manage.py::

    #!/usr/bin/env python
    if __name__ == "__main__":
        from atelier.djangoconf import manage
        manage(__file__ [,...] )

wsgi.py:: 

    from atelier.djangoconf import configure 
    configure(__file__ [,...] )
    import django.core.handlers.wsgi
    application = django.core.handlers.wsgi.WSGIHandler()
  

:copyright: Copyright 2013 by Luc Saffre.
:license: BSD, see LICENSE for more details.

"""

from atelier.djangoconf.configure import manage, configure, register_env


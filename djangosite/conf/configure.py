"""
:copyright: Copyright 2013 by Luc Saffre.
:license: BSD, see LICENSE for more details.

"""

import site
import os, sys
from os.path import split, dirname, abspath, join


class VirtualEnv(object):
    def __init__(self,name,python_version=DEFAULT_PYTHON_VERSION):
        self.name = name
        self.python_version = python_version

VIRTUAL_ENVS = dict()

def register_env(name,*args,**kw):
    if VIRTUAL_ENVS.has_key(name):
        raise Exception("Duplicate name %s" % name)
    e = VirtualEnv(name,*args,**kw)
    VIRTUAL_ENVS[name] = e
    
config_file = '/etc/atelier/config.py'

VIRTUALENV_ROOT = '/usr/local/pythonenv'
DEFAULT_PYTHON_VERSION = '2.6'
DEBUG = False
LOCAL_PYTHONPATH = '/home/luc/mypy'

if os.path.exists(config_file):
    execfile(config_file,globals())
    
#~ def configure(globals_dict,virtual_env,settings_module=None,prefix='demo_sites.'):
def configure(filename,virtual_env=DEFAULT_VIRTUALENV,settings_module=None,prefix='demo_sites.'):
    """
    :filename: Usually calling code gives `__file__` here.
    :virtual_env: The virtual environment to use
    
    """
    #~ filename = globals_dict['__file__']
    e = VIRTUAL_ENVS[virtual_env]
    p = join(VIRTUALENV_ROOT,'%s/lib/python2.6/site-packages' % (e.name,e.python_version))
    site.addsitedir(p)
    if settings_module is None:
        prj = split(dirname(abspath(filename)))[-1]
        settings_module = prefix + prj + '.settings'
    os.environ['DJANGO_SETTINGS_MODULE'] = settings_module
    if LOCAL_PYTHONPATH:
        sys.path.append(LOCAL_PYTHONPATH)

def manage(*args,**kw):
    configure(*args,**kw)
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
    

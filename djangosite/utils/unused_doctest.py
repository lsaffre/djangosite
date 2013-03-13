# -*- coding: UTF-8 -*-
## Copyright 2013 Luc Saffre
"""
No longer used. It was naive to believe that it's possible 
to reload Django's models cache inside a Python process...
"""

#~ import sys

#~ from unipath import Path

from sphinx.ext.doctest import TestDirective
from sphinx.util.nodes import set_source_info
from docutils import nodes

from django.test.simple import DjangoTestSuiteRunner
from django.utils.importlib import import_module
from django.db.models import loading
from django.conf import settings

class DjangoDocTester(object):
  
    def __init__(self):
        self.old_config = None
        self.runner = None

    def update_settings(self,settings_module_name):
        """
        This is a hack needed if you want to run tests 
        in a *single* Python process over *multiple* Django settings.
        
        Certainly not to be used in a multi-threaded environment.
        Django settings are designed to not change. 
        Changing them is dangerous.
        Expect side effects and breakage between different Django versions.
        
        """
        m = import_module(settings_module_name)
        for k in dir(m):
            if k.upper() == k:
                setattr(settings,k,getattr(m,k))
                #~ print k
        settings.SETTINGS_MODULE = settings_module_name
        #~ settings.INSTALLED_APPS[:] = m.INSTALLED_APPS
        #~ settings.SITE = m.SITE

        #~ loading.cache.__init__()
        if not loading.cache.loaded:
            return 
        #~ loading.cache.__dict__ = loading.cache.__shared_state
        loading.cache._get_models_cache.clear()
        loading.cache.app_store.clear()
        loading.cache.app_labels.clear()
        loading.cache.app_errors.clear()
        loading.cache.handled.clear()
        loading.cache.loaded = False
        #~ loading.cache.handled = {}
        loading.cache.postponed = []
        loading.cache.nesting_level = 0
        #~ loading.cache._populate()


    def setup(self,settings_module_name):
        #~ sys.path.insert(0,Path().absolute())
        #~ print sys.path
        self.update_settings(settings_module_name)
        self.runner = DjangoTestSuiteRunner(verbosity=0)
        self.runner.setup_test_environment()
        self.old_config = self.runner.setup_databases()
        
    def cleanup(self):
        self.runner.teardown_databases(self.old_config)
        self.runner.teardown_test_environment()     
        self.runner = None
        self.old_config = None
        #~ if sys.path[0] == Path().absolute():
            #~ del sys.path[0] 
        
tester = DjangoDocTester()    
    

class DjangoDoctestDirective(TestDirective):
    """
    argument : e.g. path.to.site
    
    Usage::
    
      .. djangodoctest:: foo.bar
      
    - no content
    - one argument: the Python name of the settings to import
    """
    def run(self):
        # use ordinary docutils nodes for test code: they get special attributes
        # so that our builder recognizes them, and the other builders are happy.
        assert len(self.content) == 0
        
        settings_module = self.arguments[0]
        models_module = '.'.join(settings_module.split('.')[:-1])+'.models'
        setup_code = """\
from django.conf import settings
from six import print_
from django.core.management import call_command
from djangosite.utils.doctest import tester
tester.setup('%s')
from %s import *
""" % (settings_module,models_module)

        cleanup_code = """\
tester.cleanup()
"""
        #~ print 20130305, setup_code
        nodetype = nodes.comment
        groups = ['default']
        setup_node = nodetype(setup_code, setup_code, 
            testnodetype='testsetup', groups=groups)
        cleanup_node = nodetype(cleanup_code, cleanup_code, 
            testnodetype='testcleanup', groups=groups)
        set_source_info(self, setup_node)
        set_source_info(self, cleanup_node)
        return [setup_node,cleanup_node]
      
def setup(app):
    app.add_directive('djangodoctest', DjangoDoctestDirective)
    
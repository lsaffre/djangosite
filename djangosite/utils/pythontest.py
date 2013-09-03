## Copyright 2013 by Luc Saffre.
## License: BSD, see LICENSE for more details.

"""
An extended `unittest.TestCase` to be run using `setup.py` 
in the root of a project which may contain several Django projects.

We cannot import :mod:`djangosite.utils.djangotest` here
because that's designed for unit tests within a particular Django project 
(run using `djange-admin test`).



"""
import sys
import doctest

from atelier.test import TestCase

class TestCase(TestCase):
    """
    """
    
    demo_settings_module = None
    """
    The DJANGO_SETTINGS_MODULE which serves as the central demo
    for this project.
    """
    
    
    def build_environment(self):
        env = super(TestCase,self).build_environment()
        if self.demo_settings_module:
            env.update(DJANGO_SETTINGS_MODULE=self.demo_settings_module)
        return env
        
    def setUp(self):

        if self.demo_settings_module:
            from djangosite.signals import testcase_setup
            #~ from django.test.client import Client
            #~ self.client = Client()
            #~ settings.SITE.never_build_site_cache = self.never_build_site_cache
            #~ settings.SITE.remote_user_header = 'REMOTE_USER'
            testcase_setup.send(self)
        super(TestCase,self).setUp()
        
    
    def run_docs_django_tests(self,n,**kw): 
        args = ["django-admin.py"] 
        args += ["test"]
        args += ["--settings=%s" % n]
        args += ["--failfast"]
        args += ["--traceback"]
        args += ["--verbosity=0"]
        args += ["--pythonpath=%s" % self.project_root.child('docs')]
        self.run_subprocess(args,**kw)

    def run_django_manage_test(self,db,**kw): 
        p = self.project_root.child(*db.split('/'))
        args = ["python","manage.py"] 
        args += ["test"]
        #~ args += more
        args += ["--noinput"]
        args += ["--failfast"]
        #~ args += ["--settings=settings"]
        args += ["--pythonpath=%s" % p.absolute()]
        kw.update(cwd=p)
        self.run_subprocess(args,**kw)
        
    def run_django_admin_test(self,settings_module,*args,**kw): 
        return self.run_django_admin_command(settings_module,'test',"--verbosity=0",*args,**kw)
        
    def run_django_admin_command(self,settings_module,*cmdargs,**kw): 
        args = ["django-admin.py"] 
        args += cmdargs
        args += ["--settings=%s" % settings_module]
        args += ["--noinput"]
        args += ["--failfast"]
        args += ["--traceback"]
        self.run_subprocess(args,**kw)
    

    def run_docs_doctests(self,filename):
        """
        Run a simple doctest for specified file after importing the 
        docs `conf.py` (which causes the demo database to be activated).
        
        This is used e.g. for testing pages like those below
        :doc:`/tested/index`.
        
        These tests may fail for the simple reason that the demo database
        has not been initialized (in that case, run `fab initdb`).
        """
        filename = 'docs/' + filename
        #~ p = self.project_root.child(*filename.split('/')).parent
        #~ os.environ['DJANGO_SETTINGS_MODULE']='settings'
        #~ oldcwd = os.getcwd()
        #~ self.project_root.child('docs').chdir()
        #~ p.chdir()
        #~ sys.path.insert(0,'.')
        #~ print p
        sys.path.insert(0,'docs')
        import conf # trigger Django startup
        
        if False:
            # 20130828 test cases *are* required to restore the language afterwards.
            try:
                from north.dbutils import set_language
                set_language() 
                """
                Each test case starts with the site's default language.
                Test cases are not required to restore the language afterwards.
                """
            except ImportError:
                pass # not everybody uses north

        res = doctest.testfile(filename, module_relative=False,encoding='utf-8')
        
        del sys.path[0]
        #~ os.chdir(oldcwd)

        #~ return res
        if res.failed:
            self.fail("doctest.testfile() failed. See earlier messages.")
        

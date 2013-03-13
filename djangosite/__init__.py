# -*- coding: UTF-8 -*-
## Copyright 2002-2013 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.
"""
"""

from __future__ import unicode_literals

import os
import sys
import cgi
import inspect
import datetime

from os.path import join, abspath, dirname, normpath, isdir
from decimal import Decimal

execfile(os.path.join(os.path.dirname(__file__),'..','setup_info.py'))
__version__ = SETUP_INFO['version'] # 


#~ __author__ = "Luc Saffre <luc.saffre@gmx.net>"

#~ __url__ = "http://lino.saffre-rumma.net"
#~ __url__ = "http://code.google.com/p/lino/"
#~ __url__ = "http://www.lino-framework.org"


__copyright__ = """\
Copyright (c) 2002-2013 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""

from .utils import AttrDict, ispure
    
  
#~ class BaseSite(object):
class Site(object):
    """
    Base class for the Site instance to be stored in :setting:`SITE`.
    
    A :class:`Site` describes and represents the 
    :doc:`software application </application>` 
    running on a given site (aka "project" in Django jargon).
    
    See :doc:`/usage`.
    """
    #~ """
    #~ When extending the :class:`Site` you'll may 
    #~ prefer to base it on the :class:`BaseSite` class
    #~ which doesn't call :meth:`run_djangosite_local`.
    #~ """
    
    verbose_name = None # "Unnamed Lino Application"
    """
    Used as display name to end-users at different places.
    """
    
    #~ author = None
    #~ author_email = None
    version = None
    """
    """
    
    #~ url = None
    #~ """
    #~ """
    
    #~ description = """
    #~ yet another <a href="%s">Django-Sites</a> application.""" % __url__
    #~ """
    #~ A short single-sentence description.
    #~ It should start with a lowercase letter because the beginning 
    #~ of the sentence will be generated from other class attributes 
    #~ like :attr:`verbose_name` and :attr:`version`.
    #~ """
    
    is_local_project_dir = False
    """
    This is automatically set when a :class:`Lino` is instantiated. 
    Don't override it.
    Contains `True` if this is a "local" project.
    For local projects, Lino checks for local fixtures and config directories
    and adds them to the default settings.
    """
    
    make_missing_dirs = True
    """
    Set this to False if you don't want Lino to automatically 
    create missing dirs when needed 
    (but to raise an exception in these cases, asking you to create it yourself)
    """
    
    
    #~ source_dir = None # os.path.dirname(__file__)
    #~ """
    #~ Full path to the source directory of this Lino application.
    #~ Local Lino subclasses should not override this variable.
    #~ This is used in :mod:`lino.utils.config` to decide 
    #~ whether there is a local config directory.
    #~ """
    
    #~ source_name = None  # os.path.split(source_dir)[-1]
    
    project_name = None
    """
    Read-only.
    The leaf name of your local project directory.
    """
    
    project_dir = None
    """
    Read-only.
    Full path to your local project directory. 
    Local subclasses should not override this variable.
    
    The local project directory is where 
    local configuration files are stored:
    
    - Your :xfile:`settings.py`
    - Optionally the :xfile:`manage.py` and :xfile:`urls.py` files
    - Your :xfile:`media` directory
    - Optional local :xfile:`config` and :xfile:`fixtures` directories
    """
    
    site_config = None
    """
    See :attr:`lino.ui.Site.config_site`.
    """
    
    
    languages = None 
    """
    The language distribution used on this site.
    
    This must be either `None` or an iterable of language codes.
    Examples::
    
      languages = "en de fr nl et".split()
      languages = ['en']
      
    The first language in this list will be the site's 
    default language.
    
    Changing this setting affects your database structure 
    if your application uses babel fields,
    and thus require a data migration.
    
    If this is not None, Site will 
    set the Django settings :setting:`USE_L10N` 
    and  :setting:`LANGUAGE_CODE`.
    
    See also :doc:`/date_format`.
    
    """
    
    modules = AttrDict()
    """
    A shortcut to access all installed models and actors.
    Read-only. Applications should not set this. 
    """
    
    not_found_msg = '(not installed)'

    
    
    django_settings = None
    """
    This is where Site stores the `globals()` dictionary of your
    :xfile:`settings.py` file (the one you provided when 
    calling :meth:`Site.__init__`.
    """
    
    
    startup_time = None
    """
    Don't modify this. 
    It contains the time when this this Site has been instantiated,
    iaw the startup time of this Django process.
    """
    
    def __init__(self,*args,**kwargs):
        self.init_nolocal(*args)
        self.run_djangosite_local()
        self.override_defaults(**kwargs)
        self.apply_languages()
    
    def init_nolocal(self,project_file,django_settings,*user_apps):
            
        #~ memory_db = kwargs.pop('memory_db',False)
        #~ nolocal = kwargs.pop('nolocal',False)
            
        #~ if django_settings.has_key('LINO'):
            #~ raise Exception("Oops: rename settings.LINO to settings.SITE")
        #~ if django_settings.has_key('Lino'):
            #~ raise Exception("Oops: rename settings.Lino to settings.Site")
        self.user_apps = user_apps
        self.project_dir = normpath(dirname(project_file))
        self.project_name = os.path.split(self.project_dir)[-1]
        
        #~ self.qooxdoo_prefix = '/media/qooxdoo/lino_apps/' + self.project_name + '/build/'
        #~ self.dummy_messages = set()
        #~ self._starting_up = False
        self._startup_done = False
        #~ self._response = None
        self.django_settings = django_settings
        
        self.startup_time = datetime.datetime.now()
        
        dbname  = join(self.project_dir,'default.db')
        #~ if memory_db:
            #~ dbname  = ':memory:'
        django_settings.update(DATABASES = {
              'default': {
                  'ENGINE': 'django.db.backends.sqlite3',
                  'NAME': dbname
              }
            })
        django_settings.update(INSTALLED_APPS =
            tuple(user_apps+('djangosite',)))
        
        django_settings.update(FORMAT_MODULE_PATH = 'djangosite.formats')
        #~ django_settings.update(LONG_DATE_FORMAT = "l, j F Y")
        django_settings.update(LONG_DATE_FORMAT = "l, F j, Y")
        
            
          
    def run_djangosite_local(self):
        """
        See :doc:`/djangosite_local`
        """
        #~ kwargs.pop('nolocal',None)
        try:
            from djangosite_local import setup_site
        except ImportError:
            pass
        else:
            setup_site(self)
            
    def override_defaults(self,**kwargs):
        for k,v in kwargs.items():
            if not hasattr(self,k):
                raise Exception("%s has no attribute %s" % (self.__class__,k))
            setattr(self,k,v)
            
    def apply_languages(self):
        """
        """
        #~ self.languages = value
        if self.languages is not None:
            if isinstance(self.languages,basestring):
                self.languages = self.languages.split()
            #~ lc = [x for x in self.django_settings.get('LANGUAGES' if x[0] in languages]
            #~ lc = language_choices(*self._languages)
            #~ self.update_settings(LANGUAGES = lc)
            #~ self.update_settings(LANGUAGE_CODE = lc[0][0])
            self.update_settings(LANGUAGE_CODE = self.languages[0])
            self.update_settings(USE_L10N = True)
        
        
    
            
        
    def update_settings(self,**kw):  
        """
        This may be called from within a 
        :doc:`djangosite_local.setup_site </djangosite_local>` 
        function.
        """
        self.django_settings.update(**kw)
        
    def define_settings(self,**kwargs):
        """
        Same as :meth:`update_settings`,        
        but raises an exception if a setting already exists.
        
        TODO: Currently this test is deactivated.
        
        Because it doesn't work as expected. 
        For some reason it raises a false exception when 
        :meth:`lino.ui.Site.override_defaults` 
        tries to use it `MIDDLEWARE_CLASSES`.
        Maybe because settings is being imported twice on a devserver...
        
        """
        if False:
            for name in kwargs.keys():
                if self.django_settings.has_key(name):
                    raise Exception("Tried to define existing Django setting %s" % name)
        self.django_settings.update(kwargs)
        
    def startup(self):
        """
        Start the Lino instance (the object stored as :setting:`LINO` in 
        your :xfile:`settings.py`).
        This is called exactly once from :mod:`lino.models` 
        when Django has has populated it's model cache.
        
        This code can run several times at once when running e.g. under mod_wsgi: 
        another thread has started and not yet finished `startup()`.
        
        """
        if self._startup_done:
            #~ # logger.info("Lino startup already done")
            return
            
        self._startup_done = True
        
        self.do_site_startup()
        
    def do_site_startup(self):
        """
        This method is called during site startup
        """
        from .signals import startup
        startup.send(self)
        
    def get_settings_subdirs(self,subdir_name):
        """
        Yield all (existing) directories named `subdir_name` 
        of this site's project directory and it's inherited 
        project directories.
        """
        for cl in self.__class__.__mro__:
            #~ logger.info("20130109 inspecting class %s",cl)
            if cl is not object and not inspect.isbuiltin(cl):
                pth = join(dirname(inspect.getfile(cl)),subdir_name)
                if isdir(pth):
                    yield pth
          
       

    #~ def add_dummy_message(self,s):
        #~ self.dummy_messages.add(s)

    #~ def get_app_source_file(self):
        #~ "Override this in each application"
        #~ return __file__
        
    #~ def analyze_models(self):
        #~ from lino.core.kernel import analyze_models
        #~ analyze_models()
        
        
        
    def is_installed_model_spec(self,model_spec):
        app_label, model_name = model_spec.split(".")
        return self.is_installed(app_label)

        
    
    def makedirs_if_missing(self,dirname):
        """
        Make missing directories if they don't exist 
        and if :attr:`make_missing_dirs` is `True`.
        """
        #~ if not os.path.exists(dirname):
            #~ os.makedirs(dirname)
        if not os.path.isdir(dirname):
            if self.make_missing_dirs:
                os.makedirs(dirname)
            else:
                raise Exception("Please create yourself directory %s" % dirname)
        
    
        
        
    def is_installed(self,app_label):
        """
        Return `True` if :setting:`INSTALLED_APPS` contains an item
        which ends with the specified `app_label`.
        """
        from django.conf import settings
        #~ if not '.' in app_label:
            #~ app_label = '.' + app_label
        for s in settings.INSTALLED_APPS:
            if s == app_label or s.endswith('.'+app_label):
            #~ if s.endswith(app_label):
                return True
        #~ print "20120703 not installed: %r" % app_label


    #~ def get_installed_modules(self):
        #~ from django.conf import settings
        #~ from django.utils.importlib import import_module
        #~ from django.utils.module_loading import module_has_submodule
        #~ for app_name in settings.INSTALLED_APPS:
            #~ app_module = import_module(app_name)
            #~ if module_has_submodule(app_module, 'models'):
                #~ yield import_module('.models', app_module)
        
    def on_each_app(self,methname,*args):
        """
        Call the named method on each module in :setting:`INSTALLED_APPS`
        that defines it.
        """
        from django.db.models import loading
        for mod in loading.get_apps():
            meth = getattr(mod,methname,None)
            if meth is not None:
                meth(self,*args)

    def demo_date(self,days=0,**offset):
        """
        Used e.g. in python fixtures.
        """
        if days:
            offset.update(days=days)
        #~ J = datetime.date(2011,12,16)
        if offset:
            return self.startup_time.date() + datetime.timedelta(**offset)
        return self.startup_time.date()
        
        
    def using(self,ui=None):
        """
        Yields a list of (name, version, url) tuples
        describing the software used on this site.
        
        The first tuple NO LONGER describes the application itself.
        
        This function is used by :meth:`using_text`
        which is used  by :meth:`welcome_text`.
        
        """
        #~ from .utils import ispure
        #~ assert ispure(self.verbose_name)
        
        #~ if self.verbose_name and self.version and self.url:
            #~ yield (self.verbose_name, self.version, self.url)
        
        import sys
        version = "%d.%d.%d" % sys.version_info[:3]
        yield ("Python",version,"http://www.python.org/")
        
        import django
        yield ("Django",django.get_version(),"http://www.djangoproject.com")
        
        #~ yield ("django-site",__version__,"http://site.lino-framework.org")
        yield (SETUP_INFO['name'],SETUP_INFO['version'],SETUP_INFO['url'])
        

    def welcome_text(self):
        """
        Text to display in a console window when Lino starts.
        """
        #~ return "Using %s." % (', '.join(["%s %s" % (n,v) for n,v,u in self.using()]))
        return "This is %s using %s." % (self.site_version(),self.using_text())
          

    def using_text(self):
        """
        Text to display in a console window when Lino starts.
        """
        return ', '.join(["%s %s" % (n,v) for n,v,u in self.using()])

    def site_version(self):
        """
        Used in footnote or header of certain printed documents.
        """
        #~ from .utils import ispure
        
        #~ if self.verbose_name and self.version and self.url:
        if self.verbose_name:
            assert ispure(self.verbose_name)
            #~ return self.verbose_name, self.version, self.url)
            if self.version:
                return self.verbose_name + ' ' + self.version
            return self.verbose_name
        
        #~ name,version,url = self.using().next()
        #~ name,version,url = self.get_application_info()
        #~ if self.verbose_name
        #~ if self.version is None:
            #~ return self.verbose_name + ' (Lino %s)' % __version__
        #~ return self.verbose_name + ' ' + self.version
        #~ return name + ' ' + version
        #~ return "Lino " + __version__
    
    #~ def call_command(self,*args,**options):
        #~ from django.core.management import call_command
        #~ call_command(*args,**options)

#~ class Site(BaseSite):
    #~ """
    #~ Base class for the Site instance to be stored in :setting:`SITE`.
    
    #~ A :class:`Site` describes and represents the 
    #~ :doc:`software application </application>` 
    #~ running on a given site (aka "project" in Django jargon).
    
    #~ See :doc:`/usage`.
    #~ """
    
    #~ def __init__(self,*args,**kwargs):
        #~ super(Site,self).__init__(*args,**kwargs)

        #~ self.run_djangosite_local(**kwargs)
        
class NoLocalSite(Site):
    """
    A Site that doesn't try to load :doc:`/djangosite_local`.
    Used e.g. in docs/settings.py
    """
    def __init__(self,*args,**kwargs):
        self.init_nolocal(*args)
        self.override_defaults(**kwargs)
        self.apply_languages()


__all__ = ['Site']

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()


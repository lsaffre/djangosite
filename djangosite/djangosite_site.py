# -*- coding: UTF-8 -*-
# Copyright 2002-2013 by Luc Saffre.
# License: BSD, see LICENSE for more details.

"""
This defines the :class:`Site` class.


"""


import os
from os.path import join, abspath, dirname, normpath, isdir
import sys
import cgi
import inspect
import datetime
import warnings
#~ from decimal import Decimal


from atelier.utils import AttrDict, ispure


class Plugin(object):
    """
    Base class for all plugins.
    See :setting:`get_installed_plugins`
    """
    site_js_snippets = []
    
    #~ def __init__(self,site):
        #~ pass
    
    def setup_site(cls,site):
        pass
        
    def before_site_startup(cls,site):
        pass
        
    def get_css_includes(self,site):
        return []
        
    def get_js_includes(self,site):
        return []
        
    def get_head_lines(cls,site,request):
        return []
    

#~ class BaseSite(object):
class Site(object):
    """
    Base class for the Site instance to be stored in :setting:`SITE`.
    
    Note about the name:
    A :class:`Site <djangosite.Site>` is 
    rather an `application <http://en.wikipedia.org/wiki/Application_software>`_
    than a `site <http://en.wikipedia.org/wiki/Website>`_. 
    We chose "site" to avoid a name clash with Django's word "app".
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
    
    #~ author = None
    #~ author_email = None
    version = None
    """
    """
    
    #~ languages = None
    #~ """
    #~ Will be overridden by :attr:`north.Site.languages`.
    #~ """
    
    url = None
    """
    The URL of the website that describes this application.
    Used e.g. in a :menuselection:`Site --> About` dialog bix.
    """
    
    #~ description = """
    #~ yet another <a href="%s">Django-Sites</a> application.""" % __url__
    #~ """
    #~ A short single-sentence description.
    #~ It should start with a lowercase letter because the beginning 
    #~ of the sentence will be generated from other class attributes 
    #~ like :attr:`verbose_name` and :attr:`version`.
    #~ """
    
    make_missing_dirs = True
    
    
    #~ source_dir = None # os.path.dirname(__file__)
    #~ """
    #~ Full path to the source directory of this Lino application.
    #~ Local Lino subclasses should not override this variable.
    #~ This is used in :mod:`lino.utils.config` to decide 
    #~ whether there is a local config directory.
    #~ """
    
    #~ source_name = None  # os.path.split(source_dir)[-1]
    
    userdocs_prefix = ''
    
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
    Overridden by :attr:`lino.ui.Site.config_site`.
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
    
    _logger = None
    
    def __init__(self,settings_globals,user_apps=[],**kwargs):
        """
        Every djangosite application calls this once it's 
        :file:`settings.py` file.
        See :doc:`/usage`.
        """
        #~ print "20130404 ok?"
        self.init_before_local(settings_globals,user_apps)
        if not kwargs.pop('no_local',False):
            self.run_djangosite_local()
        self.override_defaults(**kwargs)
        #~ self.apply_languages()
    
    #~ def init_before_local(self,project_file,django_settings,*user_apps):
    def init_before_local(self,settings_globals,user_apps):
        """
        If your `project_dir` contains no :file:`models.py`, 
        but *does* contain a `fixtures` subdir, 
        then djangosite automatically adds this as "local fixtures directory" 
        to Django's `FIXTURE_DIRS`.
        """
        if not isinstance(settings_globals,dict):
            raise Exception("""
            Oops, the first argument when instantiating a %s 
            must be your settings.py file's `globals()`
            and not %r
            """ % (self.__class__.__name__,settings_globals))
            
        if isinstance(user_apps,basestring):
            user_apps = [user_apps]
        #~ self.django_settings = dict()
        #~ self.django_settings.update(settings_globals)
        self.django_settings = settings_globals
        project_file = settings_globals['__file__']
        
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
        self.startup_time = datetime.datetime.now()
        
        dbname  = join(self.project_dir,'default.db')
        #~ if memory_db:
            #~ dbname  = ':memory:'
        self.django_settings.update(DATABASES = {
              'default': {
                  'ENGINE': 'django.db.backends.sqlite3',
                  'NAME': dbname
              }
            })
        self.django_settings.update(INSTALLED_APPS =
            tuple([str(a) for a in user_apps])+('djangosite',))
        
        #~ self.django_settings.update(SECRET_KEY="20227")
        # see :djangoticket:`20227`

        
        #~ django_settings.update(FORMAT_MODULE_PATH = 'djangosite.formats')
        #~ django_settings.update(LONG_DATE_FORMAT = "l, j F Y")
        #~ django_settings.update(LONG_DATE_FORMAT = "l, F j, Y")
        
        
        
            
          
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
        
        TODO: Currently this exception is deactivated.
        Because it doesn't work as expected. 
        For some reason 
        (maybe because settings is being imported twice on a devserver)
        it raises a false exception when 
        :meth:`lino.ui.Site.override_defaults` 
        tries to use it on `MIDDLEWARE_CLASSES`...
        
        """
        if False:
            for name in kwargs.keys():
                if self.django_settings.has_key(name):
                    raise Exception("Tried to define existing Django setting %s" % name)
        self.django_settings.update(kwargs)
        
    def get_plugin(self,q):
        """
        Return the specified plugin (or a subclass) if it is installed.
        """
        for p in self.installed_plugins:
            if isinstance(p,q): 
                return p
                
    #~ def remove_plugin(self,q):
        #~ """
        #~ Deactivate the specified plugin.
        #~ """
        #~ self.installed_plugins = tuple([p for p in self.installed_plugins if not issubclass(p,q)])
                
    def get_installed_plugins(self):
        return []
        
    #~ def get_plugin_snippets(self):
        #~ html = []
        #~ for p in self.installed_plugins:
            #~ for tplname in p.site_js_snippets:
                #~ html.append(tplname)
        
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
            #~ self.logger.info("Lino startup already done")
            return
            
        self._startup_done = True
        
        #~ try:
            #~ self.installed_plugins = tuple(self.get_installed_plugins())
        #~ except Exception,e:
            #~ import traceback
            #~ traceback.print_exc(e)
            #~ 
        
        from django.utils import importlib
        
        plugins = []
        for plugin_spec in self.get_installed_plugins():
            if isinstance(plugin_spec,basestring):
                mod_name,class_name = plugin_spec.rsplit('.',1)
                m = importlib.import_module(mod_name)
                cl = getattr(m,class_name)
                plugin_spec = cl()
            plugins.append(plugin_spec)
        self.installed_plugins = tuple(plugins)
        
        #~ for p in self.installed_plugins:
            #~ p.before_site_startup(self)
            
        #~ self.logger.info("20130418 djangosite.Site.do_site_startup() gonna send startup signal")
        from djangosite.signals import pre_startup, post_startup
        pre_startup.send(self)
        self.do_site_startup()
        #~ self.logger.info("20130418 djangosite.Site.startup() ok")
        post_startup.send(self)
        
        
    @property
    def logger(self):
        if self._logger is None:
            import logging
            self._logger = logging.getLogger(__name__)
        return self._logger

            
    def do_site_startup(self):
        """
        This method is called during site startup
        """
        pass
        
    def get_settings_subdirs(self,subdir_name):
        """
        Yield all (existing) directories named `subdir_name` 
        of this site's project directory and it's inherited 
        project directories.
        """
        
        # if local settings.py doesn't subclass Site:
        if self.project_dir != normpath(dirname(inspect.getfile(self.__class__))):
            pth = join(self.project_dir,subdir_name)
            if isdir(pth):
                yield pth
            
        for cl in self.__class__.__mro__:
            #~ logger.info("20130109 inspecting class %s",cl)
            if cl is not object and not inspect.isbuiltin(cl):
                pth = join(dirname(inspect.getfile(cl)),subdir_name)
                if isdir(pth):
                    yield pth
          
       
        
    def is_installed_model_spec(self,model_spec):
        """
        Deprecated. This feature 
        was a bit too automagic and caused bugs to pass silently. 
        See e.g. :blogref:`20131025`.
        
        """
        #~ raise DeprecationWarning
        
        warnings.warn("is_installed_model_spec is deprecated.",category=DeprecationWarning)
        
        if model_spec == 'self':
            return True
        app_label, model_name = model_spec.split(".")
        return self.is_installed(app_label)

        
    
    def makedirs_if_missing(self,dirname):
        """
        Make missing directories if they don't exist 
        and if :attr:`make_missing_dirs` is `True`.
        """
        #~ if not os.path.exists(dirname):
            #~ os.makedirs(dirname)
        if not isdir(dirname):
            if self.make_missing_dirs:
                os.makedirs(dirname)
            else:
                raise Exception("Please create yourself directory %s" % dirname)
        
    
    def add_site_attribute(self,name,default_value):
        """
        Must be called from global level of a models module.
        
        Example::
        
          from django.conf import settings
          settings.SITE.add_site_attribute('accounts_ref_length',20)
        
        """
        if hasattr(self,name):
            current = getattr(self,name)
            if type(current) != type(default_value):
                raise TypeError("Invalid type")
        else:
            setattr(self,name,default_value)
        
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
        Call the named method on the `models` module of each installed 
        app. 
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
            
        #~ yield ("django-site",__version__,"http://site.lino-framework.org")
        from djangosite import SETUP_INFO
        yield (SETUP_INFO['name'],SETUP_INFO['version'],SETUP_INFO['url'])
        
        import django
        yield ("Django",django.get_version(),"http://www.djangoproject.com")
        
        import sys
        version = "%d.%d.%d" % sys.version_info[:3]
        yield ("Python",version,"http://www.python.org/")
        

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


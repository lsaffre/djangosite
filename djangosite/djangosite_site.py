# -*- coding: UTF-8 -*-
# Copyright 2002-2013 by Luc Saffre.
# License: BSD, see LICENSE for more details.

"""
This defines the :class:`Site` class.

"""

import logging
logger = logging.getLogger(__name__)

import os
from os.path import normpath, dirname, exists, join, isdir
# from os.path import join, abspath, dirname, normpath, isdir
# import sys
# import cgi
import inspect
import datetime
import warnings
#~ from decimal import Decimal
from urllib import urlencode


from atelier.utils import AttrDict, ispure


class App(object):

    """Base class for all plugins.

    Every Django app which defines a class object called "App" in its
    main module (not in the models module) is a plugin.

    Corollaire: There is at most one plugin per app, and plugins
    can be referenced using their app_label.

    TODO: rename this class (and the expected name) to "Plugin"

    Plugins get some special functionality: their App class object
    will be instiantiated exactly once when the :class:`Site`
    instantiates (i.e. before Django settings are ready), and this
    object is stored in :setting:`settings.SITE.plugins <plugins>`
    using the `app_label` as key.

    """

    media_base_url = None
    """
    Remote URL base for library media files.
    """

    media_root = None

    media_name = None
    """
    Set this to a nonempty string to use as the name of the media directory
    for this App.
    Used only by Lino applications.
    Will be ignored if `media_base_url` is nonempty.
    """

    site_js_snippets = []
    """
    List of js snippets to be injected into the `lino_*.js` file.
    """

    extends = None
    """
    The full name of an app from which this app inherits.
    They must have the same "app_label"
    """

    verbose_name = None
    """
    TODO: if this is not None, then Lino will automatically 
    add a UserGroup.
    """

    depends = None
    """
    TODO: A list of names of apps that this app depends on.
    Lino will automatically add these to your 
    `INSTALLED_APPS` if necessary.
    Note that Lino will add them *after* your app.
    To have them *before* your app, specify them explicitly.
    
    """

    extends_models = None
    """
    If specified, a list of modlib model names for which this
    app provides a subclass.
    
    For backwards compatibility this has no effect
    when :setting:`override_modlib_models` is set.
    """

    def __init__(self, site, app_label):
        """
        This is called when the Site object *instantiates*, i.e.
        you may not yet import `django.conf.settings`.
        But you get the `site` object which being instiantiated.
        """
        self.app_label = app_label
        self.site = site

    def before_site_startup(cls, site):
        pass

    def get_css_includes(self, site):
        return []

    def get_js_includes(self, settings, language):
        return []

    def get_head_lines(cls, site, request):
        return []

    def configure(self, **kw):
        """
        Set the given parameters of this App instance,
        raising an exception if caller specified invalid
        attribute name.
        """
        for k, v in kw.items():
            if not hasattr(self, k):
                raise Exception("%s has no attribute %s" % (self, k))
            setattr(self, k, v)

    def build_media_url(self, *parts):
        if self.media_base_url:
            return self.media_base_url + '/'.join(parts)
        return self.buildurl('media', self.media_name, *parts)

    def buildurl(self, *args, **kw):
        url = self.site.site_prefix + ("/".join(args))
        if len(kw):
            url += "?" + urlencode(kw)
        return url

    def setup_media_links(self, ui, urlpatterns):

        if self.media_name is None:
            return

        if self.media_base_url:
            return

        source = self.media_root
        if not source:
            # raise Exception("%s.media_root is not set." % self)
            return
        if not exists(source):
            raise Exception(
                "Directory %s (specified in %s.media_root) does not exist" %
                (source, self))
        ui.setup_media_link(
            urlpatterns,
            self.media_name, source=self.media_root)




#~ class BaseSite(object):
class Site(object):

    """
    Base class for the Site instance to be stored in :setting:`SITE`.

    See also:

    - :doc:`/usage`
    - :doc:`/settings`
    - :ref:`application`
    """

    verbose_name = None  # "Unnamed Lino Application"

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

    # ~ source_dir = None # os.path.dirname(__file__)
    #~ """
    #~ Full path to the source directory of this Lino application.
    #~ Local Lino subclasses should not override this variable.
    #~ This is used in :mod:`lino.utils.config` to decide
    #~ whether there is a local config directory.
    #~ """
    # ~ source_name = None  # os.path.split(source_dir)[-1]
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
    Overridden by :attr:`lino.lino_site.Site.site_config`.
    """

    not_found_msg = '(not installed)'

    django_settings = None

    hidden_apps = set()

    startup_time = None
    """
    Don't modify this. 
    It contains the time when this this Site has been instantiated,
    iaw the startup time of this Django process.
    """

    modules = AttrDict()
    # this is explained in the polls tutorial
    # cannot use autodoc for this attribute
    # because autodoc shows the "default" value

    _logger = None

    def __init__(self, settings_globals, user_apps=[], **kwargs):
        """
        Every djangosite application calls this once it's
        :file:`settings.py` file.
        See :doc:`/usage`.
        """
        #~ print "20130404 ok?"
        self.init_before_local(settings_globals, user_apps)
        no_local = kwargs.pop('no_local', False)
        if not no_local:
            self.run_djangosite_local()
        self.override_defaults(**kwargs)
        #~ self.apply_languages()

        if not no_local:
            try:
                from djangosite_local import setup_ui
            except ImportError:
                pass
            else:
                setup_ui(self)

    def run_djangosite_local(self):
        """
        See :doc:`/djangosite_local`
        """
        try:
            from djangosite_local import setup_site
        except ImportError:
            pass
        else:
            setup_site(self)

    def init_before_local(self, settings_globals, user_apps):
        """
        If your `project_dir` contains no :file:`models.py`,
        but *does* contain a `fixtures` subdir,
        then djangosite automatically adds this as "local fixtures directory"
        to Django's `FIXTURE_DIRS`.
        """
        if not isinstance(settings_globals, dict):
            raise Exception("""
            Oops, the first argument when instantiating a %s 
            must be your settings.py file's `globals()`
            and not %r
            """ % (self.__class__.__name__, settings_globals))

        if isinstance(user_apps, basestring):
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

        dbname = join(self.project_dir, 'default.db')
        #~ if memory_db:
            #~ dbname  = ':memory:'
        self.django_settings.update(DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': dbname
            }
        })

        #~ self.django_settings.update(SECRET_KEY="20227")
        # see :djangoticket:`20227`

        #~ django_settings.update(FORMAT_MODULE_PATH = 'djangosite.formats')
        #~ django_settings.update(LONG_DATE_FORMAT = "l, j F Y")
        #~ django_settings.update(LONG_DATE_FORMAT = "l, F j, Y")

    override_modlib_models = None

    def is_abstract_model(self, name):
        """
        Return True if the named model ("myapp.MyModel") is declared in
        :attr:`override_modlib_models`.
        """
        return name in self.override_modlib_models

    def override_defaults(self, **kwargs):

        for k, v in kwargs.items():
            if not hasattr(self, k):
                raise Exception("%s has no attribute %s" % (self.__class__, k))
            setattr(self, k, v)

        if isinstance(self.hidden_apps, basestring):
            self.hidden_apps = set(self.hidden_apps.split())

        installed_apps = tuple(self.get_installed_apps()) + \
            ('djangosite',)

        installed_apps = tuple([
            str(x) for x in installed_apps
            if not x.split('.')[-1] in self.hidden_apps])
        self.update_settings(INSTALLED_APPS=installed_apps)

        from django.utils.importlib import import_module

        plugins = []
        self.plugins = AttrDict()
        for app_name in installed_apps:
            app_mod = import_module(app_name)
            app_class = getattr(app_mod, 'App', None)
            if app_class is not None:
                # print "Loading plugin", app_name
                n = app_name.rsplit('.')[-1]
                p = app_class(self,n)
                plugins.append(p)
                self.plugins.define(n, p)
        self.installed_plugins = tuple(plugins)

        if self.override_modlib_models is None:
            self.override_modlib_models = dict()
            for p in self.installed_plugins:
                    if p.extends_models is not None:
                        for m in p.extends_models:
                            self.override_modlib_models[m] = p

            # from django.utils.importlib import import_module
            # for n in installed_apps:
            #     m = import_module(n)
            #     app = getattr(m, 'App', None)
            #     if app is not None:
            #         if app.extends_models is not None:
            #             for m in app.extends_models:
            #                 self.override_modlib_models.add(m)

    def get_installed_apps(self):
        return self.user_apps

    def update_settings(self, **kw):
        """
        This may be called from within a 
        :doc:`djangosite_local.setup_site </djangosite_local>` 
        function.
        """
        self.django_settings.update(**kw)

    def define_settings(self, **kwargs):
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
                    raise Exception(
                        "Tried to define existing Django setting %s" % name)
        self.django_settings.update(kwargs)

    def startup(self):
        """
        Start the Lino instance (the object stored as :setting:`LINO` in
        your :xfile:`settings.py`).
        This is called exactly once from :mod:`lino.models`
        when Django has has populated it's model cache.

        This code can run several times at once when
        running e.g. under mod_wsgi:
        another thread has started and not yet finished `startup()`.
        
        """
        if self._startup_done:
            #~ self.logger.info("Lino startup already done")
            return

        self._startup_done = True

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

    def get_settings_subdirs(self, subdir_name):
        """
        Yield all (existing) directories named `subdir_name` 
        of this site's project directory and it's inherited 
        project directories.
        """

        # if local settings.py doesn't subclass Site:
        if self.project_dir != normpath(dirname(
                inspect.getfile(self.__class__))):
            pth = join(self.project_dir, subdir_name)
            if isdir(pth):
                yield pth

        for cl in self.__class__.__mro__:
            #~ logger.info("20130109 inspecting class %s",cl)
            if cl is not object and not inspect.isbuiltin(cl):
                pth = join(dirname(inspect.getfile(cl)), subdir_name)
                if isdir(pth):
                    yield pth

    def is_installed_model_spec(self, model_spec):
        """
        Deprecated. This feature 
        was a bit too automagic and caused bugs to pass silently. 
        See e.g. :blogref:`20131025`.
        
        """
        if False:  # mod_wsgi interprets them as error 
            warnings.warn("is_installed_model_spec is deprecated.",
                          category=DeprecationWarning)

        if model_spec == 'self':
            return True
        app_label, model_name = model_spec.split(".")
        return self.is_installed(app_label)

    def makedirs_if_missing(self, dirname):
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
                raise Exception("Please create yourself directory %s" %
                                dirname)

    def add_site_attribute(self, name, default_value):
        """
        Must be called from global level of a models module.
        
        Example::
        
          from django.conf import settings
          settings.SITE.add_site_attribute('accounts_ref_length',20)
        
        """
        if hasattr(self, name):
            current = getattr(self, name)
            if type(current) != type(default_value):
                raise TypeError("Invalid type")
        else:
            setattr(self, name, default_value)

    def is_installed(self, app_label):
        """
        Return `True` if :setting:`INSTALLED_APPS` contains an item
        which ends with the specified `app_label`.
        """
        from django.conf import settings
        #~ if not '.' in app_label:
            #~ app_label = '.' + app_label
        for s in settings.INSTALLED_APPS:
            if s == app_label or s.endswith('.' + app_label):
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
    def on_each_app(self, methname, *args):
        """
        Call the named method on the `models` module of each installed 
        app. 
        """
        from django.db.models import loading
        for mod in loading.get_apps():
            meth = getattr(mod, methname, None)
            if meth is not None:
                meth(self, *args)

    def demo_date(self, days=0, **offset):
        """
        Used e.g. in python fixtures.
        """
        if days:
            offset.update(days=days)
        #~ J = datetime.date(2011,12,16)
        if offset:
            return self.startup_time.date() + datetime.timedelta(**offset)
        return self.startup_time.date()

    def using(self, ui=None):
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
        yield (SETUP_INFO['name'], SETUP_INFO['version'], SETUP_INFO['url'])

        import django
        yield ("Django", django.get_version(), "http://www.djangoproject.com")

        import sys
        version = "%d.%d.%d" % sys.version_info[:3]
        yield ("Python", version, "http://www.python.org/")

    def welcome_text(self):
        """
        Text to display in a console window when Lino starts.
        """
        #~ return "Using %s." % (', '.join(["%s %s" % (n,v) for n,v,u in self.using()]))
        return "This is %s using %s." % (self.site_version(), self.using_text())

    def using_text(self):
        """
        Text to display in a console window when Lino starts.
        """
        return ', '.join(["%s %s" % (n, v) for n, v, u in self.using()])

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

    def configure_plugin(self, app_label, **kw):
        p = self.plugins.get(app_label, None)
        if p is not None:
            p.configure(**kw)

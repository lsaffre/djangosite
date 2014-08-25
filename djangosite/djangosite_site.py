# -*- coding: UTF-8 -*-
# Copyright 2002-2014 Luc Saffre.
# License: BSD, see LICENSE for more details.

"""
This defines the  :class:`Plugin` and  :class:`Site` classes.

"""

# from __future__ import unicode_literals
# from __future__ import print_function

# import logging
# logger = logging.getLogger(__name__)

import os
from os.path import normpath, dirname, join, isdir
import inspect
import datetime
import warnings


from atelier.utils import AttrDict, ispure, date_offset

PLUGIN_CONFIGS = {}


def configure_plugin(app_label, **kwargs):
    cfg = PLUGIN_CONFIGS.setdefault(app_label, {})
    cfg.update(kwargs)


class Plugin(object):
    "See :class:`ad.Plugin`."

    # extends = None
    # """
    # The full name of an app from which this app inherits.
    # They must have the same "app_label"
    # """

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
    """If specified, a list of model names for which this app provides a
    subclass.
    
    For backwards compatibility this has no effect
    when :setting:`override_modlib_models` is set.

    """

    def __init__(self, site, app_label, app_name, app_module):
        """This is called when the Site object *instantiates*, i.e.  you may
        not yet import `django.conf.settings`.  But you get the `site`
        object being instantiated.

        """
        # site.logger.info("20140226 djangosite.Plugin.__init__() %s",
        #                  app_label)
        if site._startup_done:
            raise Exception(20140227)
        self.site = site
        self.app_name = app_name
        self.app_label = app_label
        self.app_module = app_module
        if self.verbose_name is None:
            self.verbose_name = app_label.title()
        # import pdb; pdb.set_trace()
        # super(Plugin, self).__init__()

    def configure(self, **kw):
        for k, v in kw.items():
            if not hasattr(self, k):
                raise Exception("%s has no attribute %s" % (self, k))
            setattr(self, k, v)

    def get_used_libs(self, html=None):
        return []

    def on_site_startup(self, site):
        pass

    def extends_from(self):
        # return the name of the module from which this module inherits.
        for p in self.__class__.__bases__:
            if issubclass(p, Plugin):
                return p.__module__
        raise Exception("20140825 extends_from failed")


class Singleton(type):
    # thanks to http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Site(object):
    """
    See :class:`dd.Site`.

    See also:

    - :doc:`/usage`
    - :doc:`/settings`
    - :ref:`application`
    """

    # __metaclass__ = Singleton

    the_demo_date = None
    verbose_name = None  # "Unnamed Lino Application"
    version = None
    url = None
    make_missing_dirs = True
    userdocs_prefix = ''
    project_name = None
    project_dir = None

    site_config = None  # Overridden by `lino.lino_site.Site.site_config`.

    not_found_msg = '(not installed)'

    django_settings = None

    # hidden_apps = set()

    startup_time = None

    plugins = None

    modules = AttrDict()
    # this is explained in the polls tutorial
    # cannot use autodoc for this attribute
    # because autodoc shows the "default" value

    _logger = None

    def __init__(self, settings_globals, user_apps=[], **kwargs):
        """
        Every djangosite application calls this once in it's
        :file:`settings.py` file.
        See :doc:`/usage`.
        """
        # self.logger.info("20140226 djangosite.Site.__init__() a %s", self)
        #~ print "20130404 ok?"
        self.init_before_local(settings_globals, user_apps)
        no_local = kwargs.pop('no_local', False)
        if not no_local:
            self.run_djangosite_local()
        self.override_defaults(**kwargs)
        self.load_plugins()
        #~ self.apply_languages()
        self.setup_plugins()
        # self.logger.info("20140226 djangosite.Site.__init__() b")
        # if len(self.logger.handlers) == 0:
        #     raise Exception(self.logger.name)

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
        self._starting_up = False
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

    def is_abstract_model(self, module_name, model_name):
        "See :func:`dd.is_abstract_model`."
        name = '.'.join(module_name.split('.')[:-1])
        name += '.' + model_name
        rv = name in self.override_modlib_models
        # self.logger.info("20140825 is_abstract_model %s -> %s", name, rv)
        return rv

    def override_defaults(self, **kwargs):
        """
        Called internally during `__init__` method.
        Also called from :mod:`djangosite.utils.djangotest`

        """
        for k, v in kwargs.items():
            if not hasattr(self, k):
                raise Exception("%s has no attribute %s" % (self.__class__, k))
            setattr(self, k, v)

    def get_apps_modifiers(self, **kw):
        "See :meth:`dd.Site.get_apps_modifiers`."
        return kw

    def load_plugins(self):
        # Called internally during `__init__` method.

        from django.utils.importlib import import_module

        installed_apps = []
        apps_modifiers = self.get_apps_modifiers()

        if hasattr(self, 'hidden_apps'):
            raise Exception("Replace hidden_apps by get_apps_modifiers()")

        def add(x):
            if isinstance(x, basestring):
                app_label = x.split('.')[-1]
                x = apps_modifiers.get(app_label, x)
                if x:
                    # convert unicode to string
                    installed_apps.append(str(x))
            else:
                # if it's not a string, then it's a iterable of strings
                for xi in x:
                    add(xi)
        for x in self.get_installed_apps():
            add(x)
        add('djangosite')
        self.update_settings(INSTALLED_APPS=tuple(installed_apps))

        plugins = []
        self.plugins = AttrDict()
        for app_name in installed_apps:
            app_mod = import_module(app_name)
            app_class = getattr(app_mod, 'Plugin', None)
            if app_class is None:
                app_class = Plugin
            # print "Loading plugin", app_name
            k = app_name.rsplit('.')[-1]
            p = app_class(self, k, app_name, app_mod)
            cfg = PLUGIN_CONFIGS.pop(k, None)
            if cfg:
                p.configure(**cfg)
            plugins.append(p)
            self.plugins.define(k, p)
        self.installed_plugins = tuple(plugins)

        if self.override_modlib_models is not None:
            raise Exception("20140825")

        self.override_modlib_models = dict()
        for p in self.installed_plugins:
                if p.extends_models is not None:
                    for m in p.extends_models:
                        if "." in m:
                            raise Exception(
                                "extends_models in %s still uses '.'" %
                                p.app_name)
                        name = p.extends_from() + '.' + m
                        self.override_modlib_models[name] = p
        # raise Exception("20140825 %s", self.override_modlib_models)

    def get_installed_apps(self):
        "See :meth:`dd.Site.get_installed_apps`."
        return self.user_apps

    def is_hidden_app(self, app_label):
        "See :func:`dd.is_hidden_app`."
        am = self.get_apps_modifiers()
        if am.get(app_label, 1) is None:
            return True

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
        "See :func:`dd.startup`."
        
        # This code can run several times at once when running
        # e.g. under mod_wsgi: another thread has started and not yet
        # finished `startup()`.
        if self._startup_done:
            # self.logger.info("20140227 Lino startup already done")
            return

        # self.override_defaults()  # 20140227

        if not self._starting_up:
            self._starting_up = True
            from djangosite.signals import pre_startup, post_startup
            pre_startup.send(self)
            self.do_site_startup()
            # self.logger.info("20140227 Site.do_site_startup() done")
            post_startup.send(self)

        self._startup_done = True

    @property
    def logger(self):
        if self._logger is None:
            import logging
            self._logger = logging.getLogger(__name__)
        return self._logger

    def setup_plugins(self):
        "See :meth:`ad.Site.setup_plugins`."
        pass

    def do_site_startup(self):
        "See :meth:`ad.Site.do_site_setup`."
        for p in self.installed_plugins:
            p.on_site_startup(self)

    def get_settings_subdirs(self, subdir_name):
        "See :meth:`ad.Site.get_settings_subdirs`."

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
        """Deprecated. This feature was a bit too automagic and caused bugs
        to pass silently.  See e.g. :blogref:`20131025`.

        """
        if False:  # mod_wsgi interprets them as error
            warnings.warn("is_installed_model_spec is deprecated.",
                          category=DeprecationWarning)

        if model_spec == 'self':
            return True
        app_label, model_name = model_spec.split(".")
        return self.is_installed(app_label)

    def makedirs_if_missing(self, dirname):
        "See :func:`dd.makedirs_if_missing`."
        if dirname and not isdir(dirname):
            if self.make_missing_dirs:
                os.makedirs(dirname)
            else:
                raise Exception("Please create yourself directory %s" %
                                dirname)

    def is_installed(self, app_label):
        "See :func:`dd.is_installed`."
        return app_label in self.plugins

    def on_each_app(self, methname, *args):
        "See :func:`dd.on_each_app`."
        from django.db.models import loading
        for mod in loading.get_apps():
            meth = getattr(mod, methname, None)
            if meth is not None:
                meth(self, *args)

    def for_each_app(self, func, *args, **kw):
        "See :func:`dd.for_each_app`."

        from django.utils.importlib import import_module
        done = set()
        for p in self.installed_plugins:
            for b in p.__class__.__mro__:
                if not b in (object, Plugin):
                    if not b.__module__ in done:
                        done.add(b.__module__)
                        parent = import_module(b.__module__)
                        func(b.__module__, parent, *args, **kw)
            if not p.app_name in done:
                func(p.app_name, p.app_module, *args, **kw)

    def demo_date(self, *args, **kwargs):
        "See :attr:`ad.Site.demo_date`."
        base = self.the_demo_date or self.startup_time.date()
        return date_offset(base, *args, **kwargs)

    def today(self):
        return self.the_demo_date or datetime.date.today()

    def get_used_libs(self, html=None):
        "See :meth:`ad.Site.get_used_libs`."
        
        from djangosite import SETUP_INFO
        yield (SETUP_INFO['name'], SETUP_INFO['version'], SETUP_INFO['url'])

        import django
        yield ("Django", django.get_version(), "http://www.djangoproject.com")

        import sys
        version = "%d.%d.%d" % sys.version_info[:3]
        yield ("Python", version, "http://www.python.org/")

    def welcome_text(self):
        "See :meth:`ad.Site.welcome_text`."
        return "This is %s using %s." % (
            self.site_version(), self.using_text())

    def using_text(self):
        "See :meth:`ad.Site.using_text`."
        return ', '.join(["%s %s" % (n, v)
                          for n, v, u in self.get_used_libs()])

    def site_version(self):
        "See :meth:`ad.Site.site_version`."
        if self.verbose_name:
            assert ispure(self.verbose_name)
            if self.version:
                return self.verbose_name + ' ' + self.version
            return self.verbose_name

    def configure_plugin(self, app_label, **kw):
        raise Exception("Replace SITE.configure_plugin by ad.configure_plugin")

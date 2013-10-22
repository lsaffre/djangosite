Usage
=====

The :mod:`djangosite` Python package is a small Django app which 
does not define any models, it just provides a `Site` class 
designed to be instantiated as ``settings.SITE``.

Installation is easy::

    pip install djangosite
    
    
To turn your Django project into a djangosite, you add two lines 
*at the beginning* of your :xfile:`settings.py` file
and add ``djangosite`` as the last item of your :setting:`INSTALLED_APPS`::

  from djangosite import Site
  SITE = Site(globals())
  # ... your settings here
  INSTALLED_APPS = ["myapp1","myapp2", "djangosite"]
  # "djangosite" must be the last item of your INSTALLED_APPS


That is, you import the :class:`Site` class 
(or some subclass, see :doc:`later </extending>`), 
then assign an instance of it to a setting variable whose 
name must be ``SITE``.

When instantiating a :class:`djangosite.Site`,
only the first parameter is mandatory 
and it should always be the `globals()`
dictionary of your :file:`settings.py`.

`djangosite` will for example read the `__file__ 
<http://docs.python.org/2/reference/datamodel.html#index-49>`__
attribute of this, to know where your :file:`settings.py` 
is in the file system.

By passing the globals dictionary of your :file:`settings.py` file
you also give djangosite the possibility to modify your Django 
settings.
Which means that if you want to modify one of these, 
do it *after* instantiating your :setting:`SITE`).
That's why we told you to instantiate your `SITE`
*at the beginning* of your :xfile:`settings.py` file

An optional second positional argument is the value of your original 
:setting:`INSTALLED_APPS`, to which `djangosite`
will automatically add itself as last item.

  from djangosite import Site
  INSTALLED_APPS = ['myapp1','myapp2']
  SITE = Site(globals(),INSTALLED_APPS)

Besides this you can override any class argument using a keyword 
argment of same name:

- title <djangosite.Site.title>
- verbose_name <djangosite.Site.verbose_name>

You've maybe heard that it is not allowed 
to modify Django's settings once it has started.
But there's nothing illegal with this here
because this happens before Django has seen your :xfile:`settings.py`.

The base class will modify the following Django settings:

- `DATABASES 
  <https://docs.djangoproject.com/en/dev/ref/settings/#databases>`_ :
  djangosite sets this to a sqlite on a file `default.db` in your 
  :attr:`project_dir <djangosite.Site.project_dir>`.
  
- `INSTALLED_APPS
  <https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps>`_
  
See also :ref:`djangosite_local.py <djangosite_local>`

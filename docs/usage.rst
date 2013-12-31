Usage
=====

Installation is easy::

    pip install djangosite
    
To turn your Django project into a djangosite, you change your
:xfile:`settings.py` file as follows:

Before::

  # ... your settings 
  INSTALLED_APPS = ["myapp1","myapp2"]
  # ... your settings 

After::

  from djangosite import Site
  SITE = Site(globals(),["myapp1","myapp2"])
  # ... your settings here

That is, you import the :class:`Site` class 
(or some subclass, see :doc:`/extending`), 
then assign an instance of it to a setting variable whose 
name *must* be ``SITE``.

When instantiating a :class:`Site <djangosite.djangosite_site.Site>`,
the first parameter must be ``globals()``, because djangosite is going
to automatically set certain Django settings:

- `DATABASES 
  <https://docs.djangoproject.com/en/dev/ref/settings/#databases>`_ :
  djangosite sets this to a sqlite on a file `default.db` in your 
  :attr:`project_dir <djangosite.Site.project_dir>`.
  
- `INSTALLED_APPS
  <https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps>`_
  
Which means that if you want to modify one of these, 
do it *after* instantiating your :setting:`SITE`).

The optional second positional argument should be the value of your
original :setting:`INSTALLED_APPS` (to which `djangosite` will
automatically add itself as last item).  If you don't specifiy this
argument, then you should specify your installed apps by overriding
:setting:`get_installed_apps`.

Besides this you can override any class argument using a keyword 
argment of same name:

- :setting:`title`
- :setting:`verbose_name`
- :setting:`hidden_apps`

You've maybe heard that it is not allowed to modify Django's settings
once it has started.  But there's nothing illegal with this here
because this happens before Django has seen your :xfile:`settings.py`.

`djangosite` does more than this. It will for example read the
`__file__
<http://docs.python.org/2/reference/datamodel.html#index-49>`__
attribute of this, to know where your :file:`settings.py` is in the
file system.

See also :ref:`djangosite_local.py <djangosite_local>`

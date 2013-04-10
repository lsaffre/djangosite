Usage
=====

To use a Django Site, you do something like the following *at the beginning* 
of your :xfile:`settings.py` file::

  from djangosite import Site
  SITE = Site(globals(),'myapp1','myapp2')
  
That is, you import the :class:`Site` class (or some subclass, see later), 
then assign an instance of it to a setting variable whose 
name must be ``SITE``.

Only the first parameter is mandatory 
and it should always be the `globals()`
dictionary of your :file:`settings.py`.

`djangosite` will for example read the `__file__ 
<http://docs.python.org/2/reference/datamodel.html#index-49>`__
attribute of this, to know where your :file:`settings.py` 
is in the file system.

By passing the globals dictionary of your :file:`settings.py` file
you also give djangosite the possibility to **modify your Django 
settings**.
Which means that if you want to modify one of these, 
do it *after* instantiating your :setting:`SITE`).
That's why we told you to instantiate your `SITE`
*at the beginning* of your :xfile:`settings.py` file


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
  
- `SECRET_KEY 
  <https://docs.djangoproject.com/en/dev/ref/settings/#secret-key>`_ :
  djangosite sets this to some trivial but non-empty value
  Changed in Django 1.5: Django will now refuse to start if SECRET_KEY is not set.
  

  


See also :doc:`djangosite_local`

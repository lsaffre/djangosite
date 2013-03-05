===========
django-site
===========

Description
-----------

`django-site` adds to Django the concept of 
":doc:`the application which is running on this 
site <application>`", 
globally accessible as ``settings.SITE``
(not to confuse with Django's `SITE_ID
<https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SITE_ID>`__ 
setting).
This is the foundation for projects like 
`django-north <http://north.lino-framework.org>`__
and the 
`Lino framework <http://www.lino-framework.org>`__.

An immediate benefit of `django-site` is to 
add an :doc:`application server startup signal <startup_signal>`.
to your Django project.



Installation
------------

Installation is easy::

    pip install django-site

Usage
-----

The :mod:`django_site` Python package is a small Django app which 
does not define any models, it just provides a :class:`Site` class 
designed to be instantiated as ``settings.SITE``.

Basic usage in your :xfile:`settings.py` file::

  from django_site import Site
  SITE = Site(__file__,globals())
  # ... your settings here
  INSTALLED_APPS = [..., "django_site"]
  # Note that "django_site" must be the last item of your INSTALLED_APPS

See :doc:`/usage` for more.

Startup signals
---------------

The base implementation does little more than to emit a 
:attr:`startup <django_site.signals.startup>`
signal when Django has populated the model cache.

You can now write code like the following 
in any `models` or `admin` 
module of your existing project::

  from django_site.signals import startup, receiver
  
  @receiver(startup)
  def my_handler(sender,**kw):
      # code to run exactly once per process at startup
        
        
Extending `django-site`
-----------------------

Another usage is to subclass the :class:`django_site.Site` class::

  from django_site import Site
  
  class MySite(Site):
      version = "1.0"
      
      def do_maintenance(self):
          # your application specific code here
          
  SITE = MySite(__file__,globals())

This simple trick adds an additional level of 
encapsulation and is used by projects like 
`django-north <http://north.lino-framework.org>`__
and the 
`Lino framework <http://www.lino-framework.org>`__.


Changes
-------

See the author's `Developer Blog 
<http://www.lino-framework.org/blog/2013>`_ 
to get detailed news about what's going here.

Sitemap
-------


.. toctree::
   :maxdepth: 2

   usage
   application
   startup_signal
   releases/index
   autodoc/index
   tested/index


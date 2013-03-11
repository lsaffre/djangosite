===========
django-site
===========

.. py2rst::

  import djangosite
  print djangosite.SETUP_INFO['long_description']



Installation
------------

Installation is easy::

    pip install django-site

Usage
-----

The :mod:`djangosite` Python package is a small Django app which 
does not define any models, it just provides a :class:`Site` class 
designed to be instantiated as ``settings.SITE``.

Basic usage in your :xfile:`settings.py` file::

  from djangosite import Site
  SITE = Site(__file__,globals())
  # ... your settings here
  INSTALLED_APPS = [..., "djangosite"]
  # Note that "djangosite" must be the last item of your INSTALLED_APPS

See :doc:`/usage` for more.



Changes
-------

See the author's `Developer Blog 
<http://www.lino-framework.org/blog/2013>`_ 
to get detailed news about what's going here.

Sitemap
-------


.. toctree::
   :maxdepth: 2

   application
   startup_signal
   usage
   extending
   djangosite_local
   releases/index
   API <api/djangosite>
   tested/index
   date_format


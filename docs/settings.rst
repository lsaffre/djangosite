.. _djangosite.settings:

====================================
Settings reference
====================================

Here is a list of attributes and methods of 
:ref:`djangosite` instance
which application developers should know.

.. setting:: verbose_name

Used as display name to end-users at different places.


.. setting:: make_missing_dirs

Set this to False if you don't want this Site to automatically 
create missing directories when needed 
(but to raise an exception in these cases, asking you to create it yourself)


.. setting:: get_installed_apps

Yield the list of apps to be installed on this site.  This will be
stored to :setting:`INSTALLED_APPS` when the Site instantiates.  

Each item must be either a string (unicode being converted to str) or
a *generator* which will be iterated recursively (again expecting
either strings or geneortaors of strings).

.. setting:: hidden_apps

A set (or space-spearated string) with the names of apps which should
*not* get installed even if :setting:`get_installed_apps` returns them.

Either an empty `set`

.. setting:: override_modlib_models

Internally used. Contains a set of model names that were 
declared to be overridden.

See also :meth:`djangosite.Site.is_abstract_model`.

.. setting:: django_settings

This is where the Site stores the `globals()` dictionary of your
:xfile:`settings.py` file (the one you provided when 
instantiating the Site object).


.. setting:: plugins

An :class:`AttrDict` object with one entry for each installed 
app that is a plugin (i.e. which has an 
:class:`ad.App <djangosite.djangosite_site.App>` class object)




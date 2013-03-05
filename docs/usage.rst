Usage
=====

A Site is usually meant to work for a given set of Django apps. 
Each Lino application defines its :setting:`INSTALLED_APPS` setting.

A Site usually also defines a Django app, but not always:
it can consist of just a settings file (e.g. :mod:`lino.projects.min1`).

This class is first defined in :mod:`django_site`, 
subclassed by :mod:`lino` and by :mod:`lino.ui`, 
then usually subclassed by the application developer
(e.g. :mod:`lino.projects.cosi.Site`),
then imported into your local :xfile:`settings.py`,
where you may subclass it another time before 
finally instantiating it, and assigning it to 
the :setting:`SITE` variable.

Instantiation is always the same line of code::

  from django_site import Site
  SITE = Site(__file__,globals())
  INSTALLED_APPS = [... "django_site"]
  
With the parameters `__file__` and `globals()` you give `django_site` 
information about your local :xfile:`settings.py` 
(where it is in the file system), 
and the possibility to modify your Django settings.

During instantiation the `Site` will modify the following Django settings 
(which means that if you want to modify one of these, 
do it *after* instantiating your :setting:`SITE`):

  :setting:`DATABASES`
  :setting:`INSTALLED_APPS`


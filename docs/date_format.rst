:orphan:

Adding a new date format
========================

(This document is obsolete. See :blogref:`20130315`)

Django knows two methods for formatting a date:

================== ============ ==============
Setting            default (en) Example
================== ============ ==============
SHORT_DATE_FORMAT  ``m/d/Y``    12/31/2003
DATE_FORMAT        ``N j, Y``   Feb. 4, 2003
================== ============ ==============

`django-site` adds a third format `LONG_DATE_FORMAT` which mentions the 
weekday and the full name of the month:

>>> from datetime import date
>>> today = date(2013,01,18)
>>> from djangosite.dbutils import dtosl
>>> print dtosl(today)
Friday, January 18, 2013

A localized setting for it is currently available in four 
other languages:

>>> from django.utils import translation 
>>> for lang in ('de','fr','nl','et'):
...     translation.activate(lang)
...     print dtosl(today)
Freitag, 18. Januar 2013
vendredi 18 janvier 2013
vrijdag, 18. januari 2013
reede, 18. jaanuar 2013.a.

(Where I am not yet sure whether they all are grammatically correct.)
Contributions for other languages are welcome.

To achieve this, `django-site` adds a new 
setting `LONG_DATE_FORMAT` and uses Django's 
:setting:`FORMAT_MODULE_PATH` setting to point to 
:mod:`djangosite.formats`.

Django's list of 
`available format strings
<https://docs.djangoproject.com/en/dev/ref/templates/builtins/#std:templatefilter-date>`__



>>> from djangosite.dbutils import dtos
>>> for lang in ('en','de','fr','nl','et'):
...     translation.activate(lang)
...     print translation.get_language(),dtos(today)
en 01/18/2013
de 18.01.2013
fr 18/01/2013
nl 18-01-2013
et 18.01.2013

Note that django-site also corrected the Dutch and the French `SHORT_DATE_FORMAT`.



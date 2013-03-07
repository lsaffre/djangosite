===========
django-site
===========

`django-site` defines a `Site` 
class which represents the application that running on 
this site. Where "application" means "a collection of apps 
which are perceived as a whole by the end-user".

An immediate benefit of the base implementation 
is to emit a `startup` signal when Django 
has finished populating the model cache.

Another possible use is to subclass the `Site` class. 
This adds an additional level of encapsulation
and is used as foundation by projects like 
`django-north <http://north.lino-framework.org>`__
and the 
`Lino framework <http://www.lino-framework.org>`__.

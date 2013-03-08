==========================
django-site README
==========================
An extensible SITE object for Django

Description
-----------

`django-site` adds to a Django project the concept of 
"the application running on this site".
It defines a :class:`djangosite.Site` class class
and expects an instance of it in ``settings.SITE``.

This brings an additional level of encapsulation to Django.
A :class:`djangosite.Site` is "something between an app and a project",
it is a kind of "master app" or "project template".
Note that it has nothing to do with Django's `SITE_ID
<https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SITE_ID>`__ 
setting.
More about this vocabulary problem in :doc:`application`.

An immediate benefit of `django-site` is to implement a
:doc:`server startup signal for Django <startup_signal>`.

`django-site` is also the foundation for projects like 
`django-north <http://north.lino-framework.org>`__
and the `Lino framework <http://www.lino-framework.org>`__.

Read more on http://site.lino-framework.org

==========================
django-site README
==========================

An extensible SITE object for Django

Description
-----------

`django-site` adds to a Django project the concept of 
"the application running on this site".
It defines a `Site` class class
and expects an instance of it in ``settings.SITE``.

This brings an additional level of encapsulation to Django.
A `Site` is "something between an app and a project",
it is a kind of "master app" or "project template".
Note that it has nothing to do with Django's `SITE_ID
<https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SITE_ID>`__ 
setting.
More about this vocabulary problem in 
`application <http://site.lino-framework.org/application.html>`_.

An immediate benefit of `django-site` is to implement a
`server startup signal for Django 
<http://site.lino-framework.org/startup_signal.html>`__

DjangoSite is also the foundation for projects like 
`North <http://north.lino-framework.org>`__
and the `Lino framework <http://www.lino-framework.org>`__.

Read more on http://site.lino-framework.org

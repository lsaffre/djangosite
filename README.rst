==========================
djangosite README
==========================

A server startup signal for Django

Description
-----------

`djangosite` adds to a Django project the concept of 
"the application running on this site".
It defines a ``Site`` class
and expects an instance of it in ``settings.SITE``
(`more <http://site.lino-framework.org/usage.html>`__)

`djangosite` has nothing to do with Django's 
`sites framework <https://docs.djangoproject.com/en/dev/ref/contrib/sites/>`__
and `SITE_ID
<https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SITE_ID>`__ setting.
More about this vocabulary problem in 
`What is a software application? 
<http://site.lino-framework.org/application.html>`__.

An immediate benefit of `djangosite` is to implement a
`server startup signal for Django 
<http://site.lino-framework.org/startup_signal.html>`__.
The base class provides a startup method which runs after Django has 
populated it's model cache. This method analyzes the installed apps 
and emits different "site started" signals.  

Last but not least:
`djangosite` brings an additional level of encapsulation to Django
and is used as the foundation for 
`North <http://north.lino-framework.org>`__
and `Lino <http://www.lino-framework.org>`__.



Read more on http://site.lino-framework.org

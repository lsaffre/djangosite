==========================
djangosite README
==========================

A server startup signal for Django

Description
-----------



:mod:`djangosite` is a small Django app which adds to Django a
powerful mechanism and a new understanding of the terms "application"
and "plugin".

It defines a ``Site`` class which represents "the application running
on this site", and a ``Plugin`` class to specify extended meta
information about each app.

`djangosite` has nothing to do with Django's `sites framework
<https://docs.djangoproject.com/en/dev/ref/contrib/sites/>`__ and
`SITE_ID
<https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SITE_ID>`__
setting.  More about this vocabulary problem in `What is a software
application?  <http://site.lino-framework.org/application.html>`__.

An immediate benefit of `djangosite` is to implement a `server startup
signal for Django
<http://site.lino-framework.org/startup_signal.html>`__.  The base
class provides a startup method which runs after Django has populated
it's model cache. This method analyzes the installed apps and emits
different "site started" signals.

The real power of `djangosite` lies in the fact that it brings an
additional level of encapsulation to Django applications and is used
as the foundation for `North <http://north.lino-framework.org>`__ and
`Lino <http://www.lino-framework.org>`__.



Read more on http://site.lino-framework.org

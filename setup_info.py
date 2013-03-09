#~ __version__ = '0.0.2'
import os

SETUP_INFO = dict(
  name = 'django-site', 
  #~ name = 'DjangoSite', # no longer used. see blog 20130309
  version = '0.0.2',
  description = "An extensible SITE object for Django",
  license = 'Free BSD',
  packages = ['djangosite'],
  author = 'Luc Saffre',
  author_email = 'luc.saffre@gmail.com',
  requires = ['Django'],
  url = "http://site.lino-framework.org",
  #~ long_description=open(os.path.join('..','README.txt')).read(),
  long_description="""\
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
and the `Lino framework <http://www.lino-framework.org>`__.""",
  #~ test_suite = 'tests.suite',
  test_suite = 'fabfile.suite',
  classifiers="""\
  Programming Language :: Python
  Programming Language :: Python :: 2.6
  Programming Language :: Python :: 2.7
  Development Status :: 4 - Beta
  Environment :: Web Environment
  Framework :: Django
  Intended Audience :: Developers
  Intended Audience :: System Administrators
  License :: OSI Approved :: BSD License
  Natural Language :: English
  Operating System :: OS Independent
  Topic :: Database :: Front-Ends
  Topic :: Software Development :: Libraries :: Application Frameworks""".splitlines())

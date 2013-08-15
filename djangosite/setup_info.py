"""
This module is being execfile'd from `setup.py`, `djangosite/__init__.py`
and possibly some external tools, too.

:copyright: Copyright 2013 by Luc Saffre.
:license: BSD, see LICENSE for more details.
"""
SETUP_INFO = dict(
  name = 'djangosite', 
  version = '0.1.7', # released 20130813
  #~ install_requires = ['atelier==0.0.2','Django>=1.5,<1.6','Sphinx','unipath','python_dateutil'],
  install_requires = ['atelier','Django','Sphinx','unipath','python_dateutil'],
  description = "A server startup signal for Django",
  license = 'Free BSD',
  test_suite = 'tests',
  author = 'Luc Saffre',
  author_email = 'luc.saffre@gmail.com',
  url = "http://site.lino-framework.org",
  long_description="""Provides a Site class designed to be subclassed 
and instantiated as `settings.SITE`. 
The base class provides a startup method which runs after Django has 
populated it's model cache. This method analyzes the installed apps 
and emits different "site started" signals.  

`djangosite` adds to a Django project the concept of 
"the application running on this site".
It defines a `Site` class
and expects an instance of it in ``settings.SITE``.

This brings an additional level of encapsulation to Django.
A `Site` is "something between an app and a project",
it is a kind of "master app" or "project template".
Note that it has nothing to do with Django's `SITE_ID
<https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SITE_ID>`__ 
setting.
More about this vocabulary problem in 
`What is a software application? 
<http://site.lino-framework.org/application.html>`__.

An immediate benefit of `djangosite` is to implement a
`server startup signal for Django 
<http://site.lino-framework.org/startup_signal.html>`__

`djangosite` is also the foundation for projects like 
`North <http://north.lino-framework.org>`__
and the `Lino framework <http://www.lino-framework.org>`__.""",
  #~ test_suite = 'tests.suite',
  #~ test_suite = 'fabfile.suite',
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

SETUP_INFO.update(packages = [str(n) for n in """
djangosite
djangosite.management
djangosite.management.commands
djangosite.utils
djangosite.conf
""".splitlines() if n])
  


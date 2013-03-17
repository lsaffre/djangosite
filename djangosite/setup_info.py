import os

PACKAGES = [str(n) for n in """
djangosite
djangosite.management
djangosite.utils
djangosite.management.commands
""".splitlines() if n]
  
SETUP_INFO = dict(
  name = 'djangosite', 
  version = '0.1.0',
  install_requires = ['Django','six','Sphinx','unipath','python_dateutil'],
  description = "A server startup signal for Django",
  license = 'Free BSD',
  packages = PACKAGES,
  author = 'Luc Saffre',
  author_email = 'luc.saffre@gmail.com',
  url = "http://site.lino-framework.org",
  #~ long_description=open(os.path.join('..','README.txt')).read(),
  long_description="""\
`django-site` adds to a Django project the concept of 
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

An immediate benefit of `django-site` is to implement a
`server startup signal for Django 
<http://site.lino-framework.org/startup_signal.html>`__

`django-site` is also the foundation for projects like 
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

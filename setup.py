import os
from setuptools import setup

execfile(os.path.join(os.path.dirname(__file__),'djangosite','version.py'))

setup(name = 'django-site',
  version = __version__,
  description = "An extensible SITE object for Django",
  license = 'Free BSD',
  packages = ['djangosite'],
  author = 'Luc Saffre',
  author_email = 'luc.saffre@gmail.com',
  requires = ['Django'],
  url = "http://site.lino-framework.org",
  long_description=open('README.txt').read(),
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

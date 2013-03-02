import os
from setuptools import setup
#~ from distutils.core import setup
#~ from distribute.core import setup

execfile(os.path.join(os.path.dirname(__file__),'django_site','version.py'))

setup(name = 'django-site',
  version = __version__,
  description = "",
  license = 'Free BSD',
  packages = ['django_site'],
  author = 'Luc Saffre',
  author_email = 'luc.saffre@gmail.com',
  requires = ['Django'],
  url = "http://site.lino-framework.org",
  #~ test_suite = 'lino.test_apps',
  classifiers="""\
  Programming Language :: Python
  Programming Language :: Python :: 2
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

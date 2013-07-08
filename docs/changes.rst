.. _djangosite.changes: 

=======================
Changes in `djangosite`
=======================

Version 0.1.6 (not yet released)
============================================

- In :class:`djangosite.utils.djangotest.TestCase`, added 
  new attribute 
  :attr:`override_djangosite_settings <djangosite.utils.djangotest.TestCase.override_djangosite_settings>`
  and removed 
  attribute `never_build_site_cache` which is no longer relevant.


Version 0.1.5 (released :blogref:`20130527`)
============================================

Version 0.1.4 (released :blogref:`20130515`)
============================================

- New module :mod:`djangosite.utils.pythontest`
  contains code which was previously in :mod:`atelier.test`.

Version 0.1.3 (released :blogref:`20130505`)
============================================

Version 0.1.2 (released :blogref:`20130422`)
============================================

- Instantiating a `djangosite.Site` now sets a trivial default value 
  for `SECRET_KEY`. See :blogref:`20130409`.

- Existing instances must adapt their local `settings.py` files.
  See :blogref:`20130405`.

- :mod:`djangosite.utils.fablib` now supports an optional 
  internationalized "user manual" per project.
  See :blogref:`20130401`.
  
- Changes in :mod:`djangosite.utils.sphinxconf`.

- Moved the set_language function from north to djangosite because 
  it is used in :mod:`djangosite.utils.sphinxconf`.

- Adapted copyright headers. 
  Replaced the `/releases` directory by a single file `/changes.rst`.
  :mod:`djangosite.utils.fablib` no longer insists on calling `write_release_notes`.
  See :blogref:`20130331`.

Version 0.1.1 (released 2013-03-29)
===================================

- Changes before 0.1.1 are not listed here.
  See the developers blog and/or the Mercurial log.

  This project was split out of 
  `Lino <https://pypi.python.org/pypi/lino>` in 
  March 2013.
  


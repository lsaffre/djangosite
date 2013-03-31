"""
This defines the :class:`DocTest` class.

:copyright: Copyright 2013 by Luc Saffre.
:license: BSD, see LICENSE for more details.
"""

#~ from djangosite.utils.test import DocTest

import os
import unittest
import doctest

from django.conf import settings

class DocTest(unittest.TestCase):
    """
    Looks for a file "index.rst" in your project_dir and (if it exists) 
    run doctest on it.
    """
    doctest_files = ["index.rst"]
    def test_files(self):
        #~ g = dict(print_=six.print_)
        g = dict()
        g.update(settings=settings)
        for n in self.doctest_files:
            f = os.path.join(settings.SITE.project_dir,n)
            if os.path.exists(f):
                #~ print f
                res = doctest.testfile(f,module_relative=False,globs=g)
                if res.failed:
                    self.fail("Failed doctest %s" % f)
        
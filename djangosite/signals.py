"""
This defines the :attr:`startup` signal.

:copyright: Copyright 2013 by Luc Saffre.
:license: BSD, see LICENSE for more details.
"""

from django.dispatch import Signal, receiver

pre_startup = Signal()
post_startup = Signal()
#~ startup = Signal()
"""
Sent exactly once per process at site startup, 
just before any application-specific startup actions.

sender: 
  the Site instance
  
"""

testcase_setup = Signal()
"""
Emitted each time `djangosite.utils.TestCase.setUp` is called.
lino.ui.Site uses this signal to reset its SiteConfig cache.
It is necessary because (afaics) the Django test runner doesn't 
send a 'connected' signal when it restores the database to a 
virgin state before running a new test case.
"""

database_ready = Signal()

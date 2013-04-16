from django.dispatch import Signal
testcase_setup = Signal()
"""
Emitted each time `djangosite.utils.TestCase.setUp` is called.
lino.ui.Site uses this signal to reset its SiteConfig cache.
It is necessary because (afaics) the Django test runner doesn't 
send a 'connected' signal when it restores the database to a 
virgin state before running a new test case.
"""


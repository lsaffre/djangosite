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


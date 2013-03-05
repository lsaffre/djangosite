# -*- coding: UTF-8 -*-
## Copyright 2009-2013 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""

"""

from __future__ import unicode_literals


class AttrDict(dict):
    """
    Dictionary-like helper object.
    
    Usage example:
    
    >>> from django_site.utils import AttrDict
    >>> a = AttrDict()
    >>> a.define('foo',1)
    >>> a.define('bar','baz',2)
    >>> print a
    {'foo': 1, 'bar': {'baz': 2}}
    >>> print a.foo
    1
    >>> print a.bar.baz
    2
    >>> print a.resolve('bar.baz')
    2
    >>> print a.bar
    {'baz': 2}
    
    """
  
    def __getattr__(self, name):
        #~ if self.has_key(name):
        return self[name]
        #~ raise AttributeError("%r has no attribute '%s'" % (self,name))
        
    def define2(self,name,value):
        return self.define(*name.split('.')+[value])
        
    def define(self,*args):
        "args must be a series of names followed by the value"
        assert len(args) >= 2
        d = s = self
        for n in args[:-2]:
            d = s.get(n,None)
            if d is None:
                d = AttrDict()
                s[n] = d
            s = d
        oldvalue = d.get(args[-2],None)
        #~ if oldvalue is not None:
            #~ print 20120217, "Overriding %s from %r to %r" % (
              #~ '.'.join(args[:-1]),
              #~ oldvalue,
              #~ args[-1]
              #~ )
        d[args[-2]] = args[-1]
        return oldvalue
    
    def resolve(self,name,default=None):
        """
        return an attribute with dotted name
        """
        o = self
        for part in name.split('.'):
            o = getattr(o,part,default)
            # o = o.__getattr__(part)
        return o



def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()


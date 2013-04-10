Assigning float values to a DecimalField
========================================

This document shows that the following bug has been removed:

    In older Django versions it wasn't a good idea to 
    assign float values to a DecimalField because 
    although Django doesn't complain at first, and although the 
    values get stored in the instance object, you'll get 
    a TypeError when you try to save the object::

      >> a = A(price=2.50,qty=8.0)
      >> a.total()
      20.00
      >> a.save() #doctest: +IGNORE_EXCEPTION_DETAIL
      Traceback (most recent call last):
      ...
      TypeError: Cannot convert float to Decimal.  First convert the float to a string  
      

This test article uses a single model:

.. literalinclude:: models.py

.. 
  >>> from tested.float2decimal.models import *


It is okay to assign integer values to DecimalFields:

>>> a = A(price=10,qty=2)
>>> a.total()
20

>>> a.save()
>>> pk = a.pk
>>> a = A.objects.get(pk=pk)
>>> a.total()
Decimal('20')

>>> a = A(price=2.50,qty=8.0)
>>> a.total()
20.0
>>> a.save()

>>> import decimal
>>> a = A(price=decimal.Decimal('2.50'),qty=8)
>>> a.total()
Decimal('20.00')
>>> a.save()

>>> a = A(price=decimal.Decimal('2.20'),qty=decimal.Decimal('2.2'))
>>> a.total()
Decimal('4.840')
>>> a.save()


Usage
=====

To use a Django Site, you do something like the following *at the beginning* 
of your :xfile:`settings.py` file::

  from djangosite import Site
  SITE = Site(__file__,globals(),'myapp1','myapp2')
  
That is, you import the :class:`Site` class (or some subclass, see later), 
then assign an instance of it to a setting variable whose 
name must be ``SITE``.

The first parameter must be 
`__file__ <http://docs.python.org/2/reference/datamodel.html#index-49>`__
attribute.
This is the shortest way to tell `djangosite` 
where your local :xfile:`settings.py` 
is in the file system.

The second parameter must always be `globals()`.
By passing your globals dictionary you give djangosite 
the possibility to **modify your Django settings**.
Which means that if you want to modify one of these, 
do it *after* instantiating your :setting:`SITE`).
That's why we told you to instantiate your `SITE`
*at the beginning* of your :xfile:`settings.py` file

You've maybe heard that it is not allowed 
to modify Django's settings once it has started.
But there's nothing illegal with this here
because this happens before Django has seen your :xfile:`settings.py`.

The base class will modify the following Django settings 

  :setting:`DATABASES`
  :setting:`INSTALLED_APPS`


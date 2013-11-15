====================================
Settings reference
====================================

Here is a list of attributes and methods of 
:ref:`djangosite` instance
which application developers should know.

.. setting:: make_missing_dirs

Set this to False if you don't want this Site to automatically 
create missing directories when needed 
(but to raise an exception in these cases, asking you to create it yourself)


.. setting:: get_installed_plugins

Yield the list of plugins to be installed on this site.
Every item should be 

- either an instance of some :class:`Plugin` subclass
- or a **string** designating a full class name.
  This class will then be imported and instantiated without any 
  arguments during :meth:`Site.startup`.
  


Example usage::

    def get_installed_plugins(self):
        for p in super(Site,self).get_installed_plugins():
            yield p
        yield 'lino.mixins.beid.BeIdReaderPlugin'
        from foo.bar import MyPlugin
        yield MyPugin(a=1,b=2)


.. setting:: verbose_name

Used as display name to end-users at different places.


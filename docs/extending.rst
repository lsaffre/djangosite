Extending `djangosite`
=======================

Another usage is to subclass the :class:`djangosite.Site` class::

  from djangosite import Site
  
  class MySite(Site):
      version = "1.0"
      def do_maintenance(self):
          # your application specific code here
          
  SITE = MySite(__file__,globals())

TODO: write more. 
Meanwhile you can look how North and Lino do it.



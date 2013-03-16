# pro-forma settings file.
#~ from djangosite import NoLocalSite as Site
from djangosite import Site
#~ SITE = Site(__file__,globals(),languages="en de fr nl et",no_local=True)
SITE = Site(__file__,globals(),no_local=True)

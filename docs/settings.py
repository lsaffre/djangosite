# pro-forma settings file.
#~ from djangosite import NoLocalSite as Site
from djangosite import Site
#~ SITE = Site(__file__,globals(),languages="en de fr nl et",no_local=True)
SITE = Site(globals(),no_local=True)
SECRET_KEY = "20227" # see :djangoticket:`20227`

# pro-forma settings file.
from djangosite import NoLocalSite as Site
SITE = Site(__file__,globals(),languages="en de fr nl et")

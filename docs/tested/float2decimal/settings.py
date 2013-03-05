from django_site import Site
SITE = Site(__file__,globals())
INSTALLED_APPS = [ 'tested.float2decimal','django_site']

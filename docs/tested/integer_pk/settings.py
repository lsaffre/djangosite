from django_site import Site
SITE = Site(__file__,globals())
INSTALLED_APPS = [ 'tested.integer_pk','django_site']

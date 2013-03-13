from djangosite.utils.fablib import *
setup_from_project()  

env.django_doctests.append('tested.float2decimal.settings')
env.django_doctests.append('tested.integer_pk.settings')

env.simple_doctests.append('djangosite/utils/__init__.py')
env.simple_doctests.append('djangosite/utils/rstgen.py')

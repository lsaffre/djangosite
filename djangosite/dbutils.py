# -*- coding: UTF-8 -*-
"""
This defines some utilities which require Django settings to be importable.

:copyright: Copyright 2013 by Luc Saffre.
:license: BSD, see LICENSE for more details.
"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import os
import sys
import datetime


from django.db import models
from django.conf import settings
from django.db.models import Q
from django.db.models.fields import FieldDoesNotExist
from django.db.models import loading
#~ from django.utils.formats import get_format
#~ from django.utils.formats import date_format
from django.template import defaultfilters
from django.utils import translation

from djangosite import DJANGO_DEFAULT_LANGUAGE, assert_django_code

from django.core.validators import validate_email, ValidationError, URLValidator
validate_url = URLValidator()
def is_valid_url(s):
    try:
        validate_url(s)
        return True
    except ValidationError:
        return False
        
def is_valid_email(s):
    try:
        validate_email(s)
        return True
    except ValidationError:
        return False
        
        
    
def is_devserver():
    """
    Returns True if we are running a development server.
    
    Thanks to Aryeh Leib Taurog in 
    `How can I tell whether my Django application is running on development server or not?
    <http://stackoverflow.com/questions/1291755>`_
    
    My additions:
    
    - Added the `len(sys.argv) > 1` test because in a 
      wsgi application the process is called without arguments.
    - Not only for `runserver` but also for `testserver` and `test`.
    
    """
    #~ print 20130315, sys.argv[1]
    return len(sys.argv) > 1 and sys.argv[1] in ('runserver','testserver','test',"makescreenshots")



def full_model_name(model,sep='.'):
    """Returns the "full name" of the given model, e.g. "contacts.Person" etc.
    """
    return model._meta.app_label + sep + model._meta.object_name
    
    
    
def obj2unicode(i):
    """Returns a user-friendly unicode representation of a model instance."""
    return u'%s "%s"' % (i._meta.verbose_name,unicode(i))
    
def obj2str(i,force_detailed=False):
    """
    Returns a human-readable ascii string representation of a model instance, 
    even in some edge cases.
    """
    if not isinstance(i,models.Model): 
        if isinstance(i,long): return str(i) # AutoField is long on mysql, int on sqlite
        if isinstance(i,datetime.date): return i.isoformat()
        if isinstance(i,unicode): return repr(i)[1:]
        return repr(i)
    if i.pk is None:
        force_detailed = True
    if not force_detailed:
        if i.pk is None:
            return '(Unsaved %s instance)' % (i.__class__.__name__)
        try:
            return u"%s #%s (%s)" % (i.__class__.__name__,str(i.pk),repr(unicode(i)))
        except Exception,e:
        #~ except TypeError,e:
            return "Unprintable %s(pk=%r,error=%r" % (
              i.__class__.__name__,i.pk,e)
            #~ return unicode(e)
    #~ names = [fld.name for (fld,model) in i._meta.get_fields_with_model()]
    #~ s = ','.join(["%s=%r" % (n, getattr(i,n)) for n in names])
    pairs = []
    for (fld,model) in i._meta.get_fields_with_model():
        #~ if fld.name == 'language':
            #~ print 20120905, model, fld
        if isinstance(fld,models.ForeignKey):
            v = getattr(i,fld.attname,None) # 20130709 Django 1.6b1
            #~ v = getattr(i,fld.name+"_id") 
            #~ if getattr(i,fld.name+"_id") is not None:
                #~ v = getattr(i,fld.name)
        else:
            v = getattr(i,fld.name,None) # 20130709 Django 1.6b1
        if v:
            pairs.append("%s=%s" % (fld.name,obj2str(v)))
    s = ','.join(pairs)
    #~ s = ','.join(["%s=%s" % (n, obj2str(getattr(i,n))) for n in names])
    #~ print i, i._meta.get_all_field_names()
    #~ s = ','.join(["%s=%r" % (n, getattr(i,n)) for n in i._meta.get_all_field_names()])
    return "%s(%s)" % (i.__class__.__name__,s)
    #~ return "%s(%s)" % (i.__class__,s)


def sorted_models_list():
    models_list = models.get_models() # trigger django.db.models.loading.cache._populate()
    def fn(a,b):
        return cmp(full_model_name(a),full_model_name(b))
    models_list.sort(fn)
    return models_list

def models_by_base(base):
    """
    Yields a list of installed models that are 
    subclass of the given base class.
    """
    for m in models.get_models():
        if issubclass(m,base):
            yield m
    
#~ models_by_abc = models_by_base

def app_labels():
    return [a.__name__.split('.')[-2] for a in loading.get_apps()]
        

def range_filter(value,f1,f2):
    """
    Assuming a database model with two fields of same data type named 
    `f1` and `f2`, return a Q object to select those rows
    whose `f1` and `f2` encompass the given value `value`.
    """
    #~ filter = Q(**{f2+'__isnull':False}) | Q(**{f1+'__isnull':False})
    q1 = Q(**{f1+'__isnull':True}) | Q(**{f1+'__lte':value})
    q2 = Q(**{f2+'__isnull':True}) | Q(**{f2+'__gte':value})
    return Q(q1,q2)
    
def inrange_filter(fld,rng,**kw):
    """
    Assuming a database model with a field named  `fld`, 
    return a Q object to select those rows
    whose `fld` value is not null and within the given range `rng`.
    `rng` must be a tuple of list with two items
    """
    assert rng[0] <= rng[1]
    kw[fld+'__isnull']=False
    kw[fld+'__gte'] = rng[0]
    kw[fld+'__lte'] = rng[1]
    return Q(**kw)

    


#~ def dtos(d):
    #~ """
    #~ Return the specified date as a localized short string of type '15.06.2011'.
    #~ See also :doc:`/date_format`.
    #~ """
    #~ if d is None: return ''  
    #~ return date_format(d,'SHORT_DATE_FORMAT')
  
#~ def dtosl(d):
    #~ """
    #~ Return the specified date as a localized long string of type 'Wednesday, May 4, 2011'.
    #~ See also :doc:`/date_format`.
    #~ """
    #~ if d is None: return ''  
    #~ from north import babel
    #~ return date_format(d,'LONG_DATE_FORMAT')
  


def monthname(n):
    """
    Return the monthname for month # n in current language.
    """
    d = datetime.date(2013,n,1)
    return defaultfilters.date(d,'F')

def fdmy(d):
    """
    "format date as month and year" :
    return the specified date as a localized string of type 'June 2011'."""
    if d is None: return ''
    return defaultfilters.date(d,'F Y')
    
dtomy = fdmy # backward compat

def set_language(lang=None):
    """
    Thin wrapper around `django.utils.translation`.
    Activate the given language, or deactivate translations if 
    the given language is `None` or `'en-us'`.
    """
    
    if lang is None or lang == DJANGO_DEFAULT_LANGUAGE:
        #~ locale.setlocale(locale.LC_ALL,'')
        translation.deactivate()
    else:
        assert_django_code(lang)
        translation.activate(lang)
        


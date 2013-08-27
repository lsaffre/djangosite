.. _application:

===============================
What is a software application?
===============================


An application is not an app
----------------------------

Django comes with a rather special use of the word "app".
Daniel and Audrey (`Two scoops of Django <https://django.2scoops.org/>`_) 
say it in a diplomatic way:

  "It’s not uncommon for new Django developers to become understandably 
  confused by Django’s usage of the word ‘app’."

If you ask me: Django is simply wrong here. 
Django says "app" where it should say "plugin".
An application is a standalone piece of software.
`django.contrib.contenttypes` is not what everybody 
(except Django people) would call an application, it is a **plugin**.

But okay, that's basically just a vocabulary problem. 
Many Django people are more or less aware of that problem,
but it would be really much work to fix it
because the word is used in variables like
`app_label` and :setting:`INSTALLED_APPS`.
Too much work for "just a vocabulary" problem.
We have to live with it and forgive Django its oddness.
In fact Django is such a great product that 
we forgive even more oddnesses than this one.
So it's clear that they won't fix it.
They are perfectionists, but they have deadlines.

The problem with this "vocabulary" problem is that it leaves 
us with no word left for what a software application really is. 
That's why we decided to speak 
about a :class:`Site <djangosite.Site>` class and a ``SITE`` setting 
rather than an ``Application`` class and an ``APP`` setting.


So what then is a Site really? 
==============================

.. currentmodule:: djangosite

A :class:`Site` defines a `software application 
<http://en.wikipedia.org/wiki/Software_application>`_,
that is, a piece of software which is perceived as an 
entity by end-users.

The base :class:`Site <djangosite.Site>` class 
has attributes like
:attr:`Site.verbose_name` (the "short" user-visible name)
and the :attr:`Site.version` which are used by the method
:meth:`Site.welcome_text`.
It also defines a 
:meth:`Site.startup` method 
and signals, which is the 
concrete reason why you might want a bare
:class:`Site <djangosite.Site>`.

But then it is designed to be subclassed.
It is subclassed by :class:`north.Site`,
which is subclassed by :class:`lino.Site`,
which is subclassed by :class:`lino.ui.Site`,
then subclassed by the application developer
(e.g. :class:`lino.projects.cosi.settings.Site`),
then imported into a local :xfile:`settings.py`,
where the system administrator may subclass it another time 
before finally instantiating it, and assigning it to 
the :setting:`SITE` variable.

Such a Site instance would then be a "project" for Django.

This brings an additional level of encapsulation to Django.
A `Site` is a kind of "master app" or "project template".
A Site is a "collection of apps" which make up a whole.

A Site is usually meant to work for a given set of Django apps. 
There are different mechanisms to define "automatic" ways 
of building the content of :setting:`INSTALLED_APPS` setting.
(TODO: write more about it)



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
`django.contrib.contenttypes` is not an application, it is a plugin.

The problem with this is that it leaves Django users
with no word  left for what a Software application really is.

Many Django people are probably aware of that problem,
but it would be really much work to fix it
because the word is used in variables like
`app_label` and :setting:`INSTALLED_APPS`.
Too much work for "just a linguistic" problem.
So it's clear that they won't fix it.
They are perfectionists, but they have deadlines.

We have to live with it and forgive Django its oddness.
In fact Django is such a great product that 
we forgive even more oddnesses than this one.

That's why we have to speak 
about a :class:`Site <djangosite.Site>` class and a `SITE` setting 
rather than an `Application` class and an `APP` setting.


So what then is a Site really? 
==============================

.. currentmodule:: djangosite

A :class:`Site` defines a `software application 
<http://en.wikipedia.org/wiki/Software_application>`_,
that is, a piece of software which is perceived as an 
entity by end-users.

The base :class:`Site <djangosite.Site>` class 
doesn't do very much on its own.
It has attributes like
:attr:`Site.verbose_name` (the "short" user-visible name)
and the :attr:`Site.version` which are used by the method
:meth:`Site.welcome_text`.
And of course the 
:meth:`Site.startup` method and signal which is the 
concrete reason why you might want a bare
:class:`Site <djangosite.Site>`.

But then it is designed to be subclassed.
It is subclassed by :mod:`north`,
which is subclassed by :mod:`lino`,
which is subclassed by :mod:`lino.ui`,
then subclassed by the application developer
(e.g. :mod:`lino.projects.cosi`),
then imported into a local :xfile:`settings.py`,
where the system administrator may subclass it another time 
before finally instantiating it, and assigning it to 
the :setting:`SITE` variable.

Such a Site instance would then be a "project" for Django.

This brings an additional level of encapsulation to Django.
A `Site` is "something between an app and a project",
it is a kind of "master app" or "project template".

A Site is usually meant to work for a given set of Django apps. 
There are different mechanisms to define "automatic" ways 
of building the content of :setting:`INSTALLED_APPS` setting.
(TODO: write more about it)

A Site can itself define a Django app, but this is not a requirement.
It can consist of just a settings file (e.g. :mod:`lino.projects.min1`).
But even the settings file isn't necessary.


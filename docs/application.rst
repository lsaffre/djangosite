===============================
What is a software application?
===============================

An application is not an app
----------------------------

Note that "application" here has nothing to do with 
Django's rather special use of the word "app" (as in :setting:`INSTALLED_APPS`).

Daniel and Audrey (`Two scoops of Django <https://django.2scoops.org/>`_) 
say it in a diplomatic way:

  "It’s not uncommon for new Django developers to become understandably 
  confused by Django’s usage of the word ‘app’."

The cruel truth here is that Django is wrong. 
Django says "app" where it should say "plugin".
An application is a standalone piece of software.
For example `django.contrib.contenttypes` is not an application, 
it is a plugin.

It's a pity because it leaves Django users
with no word  left for what a `Software application 
<http://en.wikipedia.org/wiki/Software_application>`_ 
really is.

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

But that's why we have to speak 
about a :class:`djangosite.Site` class and a `SITE` setting 
rather than an `Application` class and an `APP` setting.


What is a Site?
===============

.. currentmodule:: djangosite

A :class:`Site` defines a `software application 
<http://en.wikipedia.org/wiki/Software_application>`_,
that is, a piece of software which is perceived as an 
entity *by an end-user*.
Software vendors might call it a product.

End users don't know about Django's :setting:`INSTALLED_APPS` setting.

A Site has attributes like

:attr:`Site.author` and :attr:`Site.author_email`
    Name and email address of the author
:attr:`Site.short_name`
    The "short" user-visible name
- :attr:`Site.version`
- :attr:`Site.description`

A Site is usually meant to work for a given set of Django apps. 
Each Lino application defines its 

A Site usually also defines a Django app, but not always:
it can consist of just a settings file (e.g. :mod:`lino.projects.min1`).

The :class:`Site <djangosite.Site>` is first defined in :mod:`djangosite`, 
subclassed by :mod:`lino` and by :mod:`lino.ui`, 
then usually subclassed by the application developer
(e.g. :mod:`lino.projects.cosi.Site`),
then imported into your local :xfile:`settings.py`,
where you may subclass it another time before 
finally instantiating it, and assigning it to 
the :setting:`SITE` variable.



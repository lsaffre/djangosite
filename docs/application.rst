===============================
What is a software application?
===============================

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

We have to live with it.
And in fact it is easy to forgive Django.
Django is such a great product that it can afford many more 
oddnesses than this one.

But that's why we have to speak 
about a :class:`django_site.Site` class and a `SITE` setting 
rather than an `Application` class and an `APP` setting.



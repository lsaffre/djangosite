The `djangosite_local.py` file
==============================

When a :class:`djangosite.Site` gets instantiated, it will try 
to import an module named "djangosite_local", and if that module exists 
and has a function named "setup_site", call this function.
This mechanism is used on servers where many djangosite sites 
are running to provde local server-wide default settings.

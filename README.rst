----------------------
pinax-satchmo-buildout
----------------------

This project aims to kick start websites using pinax and satchmo, providing the core buildout.cfg and settings files to get new projects up and running.

The buildout will create a new website using the Django 1.1, pinax from git, and satchmo from hg.

There is a sample website project based off pinax social_project which intergrates the satchmo blocks into the base.html template.


Requirements
============

    * virtualenv 

    * git

    * mercurial

    * svn

Install
=======

    * Checkout this project to any path

    * Create newproject directory ::

        mkdir newproject
        cd newproject

    * Execute create-site.sh ::

        INSTALL_DIR/create-site.sh

    * Edit website/settings.py and set database details.

      See the pinax and satchmo documentation for more configuration options.

      http://www.satchmoproject.com/docs/svn/new_installation.html

      http://pinaxproject.com/docs/dev/customization.html

    * You need to patch the django_friends models.py to resolve a conflict with a satchmo model.::

          all_src/friends/models.py
   
      edit #45::

        users = models.ManyToManyField(User)
   
      add a related name::

        users = models.ManyToManyField(User, related_name="contacts")

    * syncdb ::

        bin/django syncdb

    * build_media ::

        bin/django build_media --all

    * runserver using development settings ::

        bin/django runserver

Post install
============

It may be helpful to load the satchmo sample data to have something to work with.

load sample locale text ::

    bin/django satchmo_load_l10n

load sample store ::

    bin/django satchmo_load_store


Customize the buildout
======================

If you want to create a site using a modified buildout.cfg, 
put the buildout.cfg at the root of the project and run create-site.sh.
The script will see your buildout.cfg and not overwrite it.

It is often a good idea to set a path for download-cache in the main buildout configuration.
See http://pypi.python.org/pypi/zc.buildout#using-a-download-cache

By default buildout will store eggs in the ``eggs`` directory of the project structure.  
Using a common eggs directory allows projects to share the same eggs and makes builds much quicker.

Set the eggs-directory in the main buildout configuration to a writeable path.  
Make sure the path exists before you run buildout.


For more details on zc.buildout see:

 * http://pypi.python.org/pypi/zc.buildout

 * http://grok.zope.org/documentation/tutorial/introduction-to-zc.buildout
   
 * http://code.google.com/p/django-buildout/

 * http://github.com/pinax/pinax-buildout/tree/master

 * http://github.com/cshenton/pinax/blob/481ba59b677d5191c6e4bce54361c4aae0d5ca5e/buildout.cfg



#!/bin/sh
git clone git://github.com/hbussell/pinax-satchmo-buildout.git  /tmp/pinax-satchmo-buildout
cp /tmp/pinax-satchmo-buildout/buildout.cfg .

# bring in website settings.py, satchmo_settings.py, urls.py
# if you comment out this step a default project will be created by the djangorecipe.
# you will then need to manually copy in the settings files 
cp -R /tmp/pinax-satchmo-buildout/website/ .

virtualenv --no-site-packages env
env/bin/easy_install zc.buildout
#env/bin/easy_install MySQL-python
env/bin/buildout init
bin/buildout

#!/bin/sh
if [ ! -d "/tmp/pinax-satchmo-buildout" ]; then
    git clone git://github.com/hbussell/pinax-satchmo-buildout.git  /tmp/pinax-satchmo-buildout
fi

#if [ ! -d "~/egg-cache" ]; then
#    mkdir ~/egg-cache
#fi
#if [ ! -d "~/egg-cache/download" ]; then
#    mkdir ~/egg-cache/download
#fi
#chmod ug+rwx -R ~/egg-cache
# bring in sample project settings and templates
# if you comment out this step a default project will be created by the djangorecipe.

if [ ! -d "website" ]; then
    cp -R /tmp/pinax-satchmo-buildout/website/ .
fi

if [ ! "buildout.cfg" ]; then
    mv buildout.cfg buildout.tmp
fi

virtualenv --no-site-packages env
env/bin/easy_install zc.buildout
#env/bin/easy_install MySQL-python
env/bin/buildout init

if [ ! "buildout.tmp" ]; then
    mv buildout.tmp buildout.cfg
fi

if [ ! -f "buildout.cfg" ]; then
    cp /tmp/pinax-satchmo-buildout/buildout.cfg .
fi

bin/buildout

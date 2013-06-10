========================
Installing OpenCommunity
========================

    **Be warned:** OpenCommunity is work in progress!!

Prerequisites for Developer Machines
====================================

* git
* python 2.7 (install from http://www.ninite.com/ )

(Quick) Setup
=============

* Fork the repo and clone it to your computer using git clone
* cd into the cloned project
* You will need virtualenv.  Either install it or download virtualenv.py
  from here: https://raw.github.com/pypa/virtualenv/master/virtualenv.py
* Now create a virtualenv.  Use either::

      virtualenv .

  Or::

    python virtualenv.py .

* Good! to activate the env use this on OSX or linux::

    source bin/activate

  On windows::

    scripts\activate

* Your prompt should start with `(OpenCommunity)`.
* On windows install some binary packages first::

    windows-setup.cmd

* Now install all other requirements (This can take some time)::

    pip install -r requirements.txt

* Create a local settings file from the example file.  On linux/OSX::

    cp src/ocd/local_settings.py.example src/ocd/local_settings.py

  On windows::

    copy src\ocd\local_settings.py.example src\ocd\local_settings.py

* Now create a directory for your sqlite db::

    mkdir db

* It's time to get closer to our code::

    cd src

* ... and create the database::

    python manage.py syncdb
    python manage.py migrate

  (When asked, create a user for the admin interface)

* To start the dev web server::

    python manage.py runserver

* Profit: http://localhost:8000/

Problems
========
* You're running a command and getting " Django - “no module named django.core.management“ ". Solution: Activate env.
* Each Redirect is verbose. Solution: comment out INTERNAL_IPS = ... line in src/ocd/local_settings.py

Collaborating
=============

* Setup your git repo to get upstream changes::

    git remote add upstream git://github.com/nonZero/OpenCommunity.git
    git pull upstream master


* Now go and get them::

    git pull upstream master
    pip install -r requirements.txt
    python manage.py syncdb
    python manage.py migrate

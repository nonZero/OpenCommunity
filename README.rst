========================
Installing OpenCommunity
========================

OpenCommunity (DemOS) is an open source project that provide online tools to
real communities with elected leadership.

OpenCommunity is poweerd by `Hasadna`_.

Join the conversation in our `google group`_ (English and Hebrew).

.. _Hasadna: http://www.hasadna.org.il
.. _google group: https://groups.google.com/forum/#!forum/omiflaga

Prerequisites for Developer Machines
====================================

* git
* python 2.7 (Windows users can quickly install python from http://www.ninite.com/ )

* Install `virtualenvwrapper`:

  * On windows::

      pip install virtualenvwrapper-win

  * On ubuntu::

      sudo apt-get install virtualenvwrapper

* On ubuntu 16.04 additionally install some more requriements for pillow and pyscopg2::

    sudo apt-get install python-dev libjpeg-dev libjpeg8 zlib1g-dev libfreetype6 libfreetype6-dev libpq-dev


(Quick) Setup
=============

* Create a Python2 virtualenv::

      mkvirtualenv opencommunity

  (Note: If you both python2 and python3 installed, use the `-p` switch for
  choosing python2 to create the virtualenv)

* Fork the repo and clone it to your computer using git clone
* cd into the cloned project

* Install requirements (This can take some time)::

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

    python manage.py migrate

* Create a superuser::

    python manage.py createsuperuser

* To start the dev web server::

    python manage.py runserver

* Profit: http://localhost:8000/

Collaborating
=============

* Setup your git repo to get upstream changes::

    git remote add upstream git://github.com/hasadna/OpenCommunity.git
    git pull upstream master


* Now go and get them::

    git pull upstream master
    pip install -r requirements.txt
    python manage.py migrate


Common Problems and Solutions
=============================
* If the following message appear when running `python manage.py`::

    Django - "no module named django.core.management"
    
  You probably have not activated your virtualenv, or did not
  install the requirements.

#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source /home/oc/.virtualenvs/oc/bin/activate
cd $DIR/src
exec gunicorn -p masterpid -b 127.0.0.1:9000 -w 2 ocd.wsgi:application

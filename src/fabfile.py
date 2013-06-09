from fabric.api import *
from local_fab import code_dir, my_hosts
from contextlib import contextmanager as _contextmanager

env.hosts = my_hosts

@_contextmanager
def virtualenv(path):
    with cd(path):
        with prefix('source bin/activate'):
            yield


def host_type():
    run('uname -s')


def deploy():
    with virtualenv(code_dir):
        run("git pull")
        run("cd src && python manage.py migrate")
        run("cd src && python manage.py collectstatic --noinput")
        run("sudo supervisorctl restart opencommunity")


def log():
    run("tail %slogs/*" % code_dir)

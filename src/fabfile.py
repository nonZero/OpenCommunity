from fabric.api import *
from local_fab import code_dir, my_hosts

env.hosts = my_hosts


def host_type():
    run('uname -s')


def deploy():
    with cd(code_dir):
        run("git pull")
        run("sudo supervisorctl restart opencommunity")


def log():
    run("tail %slogs/*" % code_dir)

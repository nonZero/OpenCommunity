from fabric.api import *
code_dir = '/home/yaniv/OpenCommunity'

env.hosts = ['yaniv@oc.tiranoltd.com']

def host_type():
    run('uname -s')
    
def deploy():
    with cd(code_dir):
        run('git pull')
        run('sudo supervisorctl reload opencommunity')
        
def showlog():
    run('tail /home/yaniv/OpenCommunity/logs/OpenCommunity.log')
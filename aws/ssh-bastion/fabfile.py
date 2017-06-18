#!/usr/bin/env python3
from fabric.api import (
    env, run, put, cd, settings,
    local
)

from pprint import pprint
import json
from os import path
from io import StringIO

env.hosts = ["ec2-user@ec2-server:9022"]
env.output_prefix = False

app_name = "my-bastion"
image_name = "my-bastion.i"
remote_dir = "/home/ec2-user/.%s" % image_name

def _read_file(filepath):
    filepath = path.expanduser(filepath)
    with open(filepath, 'r') as f:
        return f.read()


def dk_build():
    dk_stop()
    dk_rm()
    run("rm -rf {0}; mkdir -p {0}/.build".format(remote_dir))
    with cd(remote_dir):
        put(path.expanduser("~/.ssh/id_rsa.pub"), ".build/id_rsa.pub")
        put("./Dockerfile", ".")
        run("docker build . -t %s" % image_name)

def dk_start():
    dk_build()
    with cd(remote_dir):
        run("docker run -dt -p 9023:22 --privileged --name %s %s"
            % (app_name, image_name))
    dk_ps()

def dk_stop():
    run("docker stop -t1 %s || true" % app_name)

def dk_logs():
    run("docker logs %s"  % app_name)

def dk_cat(file='/etc/passwd'):
    run("docker cp %s:%s %s/cat.tmp" % (app_name, file, remote_dir))
    run("cat %s/cat.tmp" % remote_dir)

def dk_ps():
    run("docker images -a")
    run("docker ps -a")

def dk_rm():
    run("docker rm  %s || true" % app_name)
    #run("docker rmi %s || true" % image_name)
    
def dk_rmi_prune():
    run("docker -v")
    # docker >= 1.13:  run("docker image prune")
    with settings(warn_only=True):
        run("docker ps -qa -f 'status=exited' | xargs docker rm")
        run("docker images -qa -f 'dangling=true' | xargs docker rmi")


def dk_clear_sshkey():
    local("ssh-keygen -f /home/dnikku/.ssh/known_hosts -R [localhost]:9023")

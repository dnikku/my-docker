#!/usr/bin/env python3
from fabric.api import (
    env, run, put, cd, settings,
    local, shell_env
)

from pprint import pprint
import json
from os import path
from io import StringIO

ssh_server = "dnikku@10.0.21.111"
env.hosts = [ssh_server]
env.output_prefix = False

app_name = "my-java"
image_name = "my-java.i"

def _read_file(filepath):
    filepath = path.expanduser(filepath)
    with open(filepath, 'r') as f:
        return f.read()

def dk_build(image=image_name):
    docker_build_dir = "/home/dnikku/.%s/build" % image_name

    run("rm -rf {0}; mkdir -p {0}".format(docker_build_dir))
    with cd(docker_build_dir):
        run("mkdir -p ssh")
        put("./ssh/*", "./ssh/")
        put("~/.ssh/id_rsa.pub", "./ssh/authorized_keys")
        put("./syslog.conf", ".")

        put("./Dockerfile", ".")
        run("docker build . -t %s" % image)

def dk_start(image=image_name, hostname=app_name, hostport=9022, rebuild=False):
    dk_stop(hostname, True)
    if rebuild:
        dk_build(image)
    run("docker run -dt -p {2}:22 -h {0} --name {0} {1}".format(hostname, image, hostport))
    dk_ps()


def dk_stop(hostname=app_name, remove=False):
    run("docker stop -t1 %s || true" % hostname)
    if remove:
        run("docker rm  %s || true" % hostname)

def dk_logs(hostname=app_name):
    run("docker logs %s"  % hostname)

def dk_ps():
    run("docker images -a")
    run("docker ps -a")

def dk_rmi_prune():
    run("docker -v")
    # docker >= 1.13:  run("docker image prune")
    with settings(warn_only=True):
        run("docker ps -qa -f 'status=exited' | xargs -r docker rm")
        run("docker images -qa -f 'dangling=true' | xargs -r docker rmi")


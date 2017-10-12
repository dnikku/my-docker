#!/usr/bin/env python3
from fabric.api import (
    env, run, put, cd, settings,
    local, shell_env
)

from pprint import pprint
import json
from os import path
from io import StringIO
from contextlib import contextmanager

#ssh_server = "dnikku@10.0.21.111"
ssh_server = "dnikku@localhost:20922"
env.hosts = [ssh_server]
env.output_prefix = False

APP_NAME = "my-lucene"
IMAGE_NAME = "my-lucene.i"

TIKA_JAR = "tika-app-1.16.jar"
TIKA_URL = "http://www.apache.org/dyn/closer.cgi/tika/%s" % TIKA_JAR
TIKA_SHA1 = "e6884af0209ace42bf0b9b59d72c3c5a0052055e"

def _read_file(filepath):
    filepath = path.expanduser(filepath)
    with open(filepath, 'r') as f:
        return f.read()

@contextmanager
def _mktemp_file():
    tmpfile = run("mktemp")
    yield tmpfile
    run("rm -f %s" % tmpfile)

def dk_build(image=IMAGE_NAME):
    docker_build_dir = "/home/dnikku/.%s/build" % image
    docker_cache_dir = "/home/dnikku/.%s/cache" % image

    with shell_env(TIKA_URL=TIKA_URL, TIKA_JAR=TIKA_JAR)
        run("echo TIKA_JAR=$TIKA_JAR")

        run("mkdir -p {0}".format(docker_cache_dir))
        with cd(docker_cache_dir):
            run("if [ ! -f $TIKA_JAR ]; then wget $TIKA_URL -O $TIKA_JAR; fi")

        run("rm -rf {0}; mkdir -p {0}".format(docker_build_dir))
        with cd(docker_build_dir):
            run("mkdir -p alpine-init")
            put("./alpine-init/*", "./alpine-init/")

            put("./Dockerfile", ".")
            run("docker build . -t %s" % image)

def dk_start(image=IMAGE_NAME, hostname=APP_NAME, hostport=9022, rebuild=False):
    dk_stop(hostname, True)
    if rebuild:
        dk_build(image)
    run("docker run -dt -p {2}:22 -h {0} --name {0} {1}".format(hostname, image, hostport))
    dk_ps()


def dk_stop(hostname=APP_NAME, remove=False):
    run("docker stop -t1 %s || true" % hostname)
    if remove:
        run("docker rm  %s || true" % hostname)

def dk_logs(hostname=APP_NAME):
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

def dk_start_dns():
    dk_stop("my-dns")
    run("docker run -d --name my-dns -h my-dns -v /var/run/docker.sock:/tmp/docker.sock -v /etc/resolv.conf:/tmp/resolv.conf mgood/resolvable")


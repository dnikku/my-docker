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

ssh_server = "dnikku@10.0.21.111"
env.hosts = [ssh_server]
env.output_prefix = False

app_name = "my-java"
image_name = "my-java.i"
hadoop_version = "2.7.3"
hadoop_package_url = "http://www-us.apache.org/dist/hadoop/common/hadoop-{0}/hadoop-{0}.tar.gz".format(hadoop_version)


def _read_file(filepath):
    filepath = path.expanduser(filepath)
    with open(filepath, 'r') as f:
        return f.read()

@contextmanager
def _mktemp_file():
    tmpfile = run("mktemp")
    yield tmpfile
    run("rm -f %s" % tmpfile)

def dk_build(image=image_name):
    docker_build_dir = "/home/dnikku/.%s/build" % image_name
    docker_cache_dir = "/home/dnikku/.%s/cache" % image_name

    with shell_env(HADOOP_VERSION=hadoop_version, HADOOP_URL=hadoop_package_url):
        run("echo HADOOP_VERSION=$HADOOP_VERSION")

        run("mkdir -p {0}".format(docker_cache_dir))
        with cd(docker_cache_dir):
            run("if [ ! -f hadoop-$HADOOP_VERSION.tar.gz ]; then wget $HADOOP_URL -O hadoop-$HADOOP_VERSION.tar.gz; fi")
            run("if [ ! -f hadoop_rsa ]; then ssh-keygen -t rsa -N '' -f hadoop_rsa -C 'hadoop@cluster'; fi")

        run("rm -rf {0}; mkdir -p {0}".format(docker_build_dir))
        with cd(docker_build_dir):
            run("mkdir -p ssh")
            put("./ssh/*", "./ssh/")
            put("~/.ssh/id_rsa.pub", "./ssh/authorized_keys")
            run("cat {0}/hadoop_rsa.pub >> ./ssh/authorized_keys".format(docker_cache_dir))
            run("cat {0}/hadoop_rsa > ./ssh/id_rsa".format(docker_cache_dir))

            run("mkdir -p python")
            put("./python/*", "./python/")

            run("mkdir -p java")
            put("./java/*", "./java/")

            put("./syslog.conf", ".")

            run("mkdir -p java")
            put("./java/*", "./java/")

            run("mkdir -p ./hadoop")
            run("cp {0}/hadoop-$HADOOP_VERSION.tar.gz ./hadoop/".format(docker_cache_dir))
            put("./hadoop/*", "./hadoop")

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

def dk_start_dns():
    dk_stop("my-dns")
    run("docker run -d --name my-dns -h my-dns -v /var/run/docker.sock:/tmp/docker.sock -v /etc/resolv.conf:/tmp/resolv.conf mgood/resolvable")

def dk_start_cluster(slaves_nr=2, image=image_name):
    master_ssh_port = 9023
    dk_stop_cluster(slaves_nr)

    run("docker run -dt -p {2}:22 -p 8088:8088 -h {0} --name {0} {1}".format("my-hd-master", image, master_ssh_port))
    for i in range(1, slaves_nr + 1):
        run("docker run -dt -h {0} --name {0} {1}".format("my-hd-slave%s" % i, image))

    with _mktemp_file() as tmp_slaves:
        local("echo 'my-hd-master' > {0}".format(tmp_slaves))
        for i in range(1, slaves_nr + 1):
            local("echo 'my-hd-slave{1}' >> {0}".format(tmp_slaves, i))
        local("cat {0}".format(tmp_slaves))
        with settings(host_string="%s:9023" % ssh_server):
            put(tmp_slaves, "~/hadoop/etc/hadoop/slaves", mode="0644")
            run("start-yarn.sh")

    dk_ps()

def dk_stop_cluster(slaves_nr=2):
    for i in range(1, slaves_nr + 1):
        dk_stop("my-hd-slave%s" % i, True)
    dk_stop("my-hd-master", True)
    dk_rmi_prune()


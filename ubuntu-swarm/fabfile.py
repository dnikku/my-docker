#!/usr/bin/env python3
from fabric.api import (
    env, run, put, cd, settings,
    local
)

from pprint import pprint
import json
from os import path
from io import StringIO


env.output_prefix = False
env.shell = "/bin/sh -l -c"

remote_dir = "/home/dnikku/.ubuntu"
boto3_machine = "dnikku@ec2-server:9023"
dk_swarm_manager = "dnikku@10.0.21.111"
dk_swarm_workers = ["dnikku@10.0.21.112", "dnikku@10.0.21.113"]

def read_file(path):
    with open(path, 'r') as f:
        return f.read()

def ec2_list():
    with settings(host_string=boto3_machine):
        run("rm -rf %s" % remote_dir)
        run("mkdir -p %s" % remote_dir)
        with cd(remote_dir):
            run("touch __init__.py")
            put("./ec2_instance.py", ".", mode="0700")
            run("python3 -c 'import ec2_instance; ec2_instance.machine_list()'")

def ec2_run():
    with settings(host_string=boto3_machine):
        run("rm -rf %s" % remote_dir)
        run("mkdir -p %s" % remote_dir)

        pub_key = read_file(path.expanduser("~/.ssh/id_rsa.pub"))
        user_data = read_file('user_data.sh').replace("{{user.pub.key}}", pub_key)
        with cd(remote_dir):
            run("touch __init__.py")
            put("./ec2_instance.py", ".", mode="0700")
            put(StringIO(user_data), "./user_data.sh")
            run("python3 -c 'import ec2_instance; ec2_instance.machine_run()'")
            #run("cat ./user_data.sh")

def dk_init_registry():
    with settings(host_string=dk_swarm_manager):
        #setup a local registry
        run("docker run -d -p 5000:5000 --restart=always --name registry registry:2")
    
def dk_swarm_init():
    with settings(host_string=dk_swarm_manager):
        dk_init_registry()
        
        host_ip = run("hostname -I | sed -En 's/(([0-9]+\\.){3}[0-9]+).*/\\1/p'")
        run("docker swarm init --advertise-addr %s" % host_ip)
        join_cmd = run("docker swarm join-token worker").replace("\\\r\n", "")
        
    for ip in dk_swarm_workers:
        dk_swarm_join(ip, join_cmd)

def dk_swarm_join(node_ip, join_cmd=None):
    if join_cmd == None:
        with settings(host_string=dk_swarm_manager):
            join_cmd = run("docker swarm join-token worker").replace("\\\r\n", "")
    with settings(host_string=ip):
        run(join_cmd)


def dk_info():
    with settings(host_string=dk_swarm_manager):
        run("docker images -a")
        run("docker ps")
        run("docker node ls")
        run("docker service ls")
        #run("docker service inspect --pretty helloworld")

def dk_start_service():
    with settings(host_string=dk_swarm_manager):
        run("docker service create --replicas 2 --name helloworld alpine ping -i 10 google.com")


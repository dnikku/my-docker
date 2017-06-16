#!/bin/sh

set -e

# generate ssh host keys
ssh-keygen -f /etc/ssh/ssh_host_rsa_key -N '' -t rsa
ssh-keygen -f /etc/ssh/ssh_host_dsa_key -N '' -t dsa
ssh-keygen -f /etc/ssh/ssh_host_ecdsa_key -N '' -t ecdsa
ssh-keygen -f /etc/ssh/ssh_host_ed25519_key -N '' -t ed25519


# disable root password
passwd -d root

# add user dnikku and setup for ssh priv key auth
adduser -D -s /bin/sh dnikku
passwd -u dnikku
chown -R dnikku:dnikku /home/dnikku
chmod -R 0700 /home/dnikku
chmod 0600 /home/dnikku/.ssh/* /home/dnikku/.aws/*

#!/bin/sh
set -e

MY_USER=dnikku

apt-get -y update

# setup python3 & boto3
apt-get -y install python3
#pip3 install --upgrade pip && pip3 install boto3

# setup ssh server
apt-get -y install openssh-server

# disable root password
passwd -d root

#add user $MY_USER and enable priv key auth
useradd -d /home/$MY_USER -s /bin/bash $MY_USER
mkdir -p /home/$MY_USER/.ssh
touch /home/$MY_USER/.ssh/authorized_key
chmod -R 0700 /home/$MY_USER
chown -R $MY_USER:$MY_USER /home/$MY_USER

chmod 0600 /home/$MY_USER/.ssh/authorized_keys


echo "Create user $MY_USER done."

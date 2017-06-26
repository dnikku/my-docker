#!/bin/sh

MY_USER=$1
MY_SSH_DIR=$2

set -e

apk add --no-cache openssh shadow
# generate host keys if not present
ssh-keygen -A

cp $MY_SSH_DIR/sshd_config /etc/ssh/sshd_config

useradd -d /home/$MY_USER -m -s /bin/bash $MY_USER
usermod -p "\$6\$*" $MY_USER

mkdir -p /home/$MY_USER/.ssh
cat $MY_SSH_DIR/authorized_keys >> /home/$MY_USER/.ssh/authorized_keys
chmod 0600 /home/$MY_USER/.ssh/authorized_keys

chown -R $MY_USER:$MY_USER /home/$MY_USER
chmod -R 0700 /home/$MY_USER

# allow user to become root (via sudo)
apk add --no-cache sudo
echo "$MY_USER ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

echo "SSH User: '$MY_USER' setup done."

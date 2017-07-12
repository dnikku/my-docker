#!/bin/bash

echo "Starting user_data.sh ..."

# fix https://stackoverflow.com/questions/2499794/how-to-fix-a-locale-setting-warning-from-perl
LC_ALL=en_US.UTF-8
LANG=en_US.UTF-8
echo "LC_ALL=en_US.UTF-8" >> /etc/environment
echo "LANG=en_US.UTF-8" >> /etc/environment

MY_USER=dnikku

#add user dnikku and enable priv key auth
useradd -d /home/$MY_USER -m -s /bin/bash $MY_USER
usermod -aG sudo $MY_USER

echo "# Created by 'user_data.sh' on $(date)

# User rules for $MY_USER
$MY_USER ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/10-$MY_USER-users

mkdir -p /home/$MY_USER/.ssh
touch /home/$MY_USER/.ssh/authorized_key
echo "{{user.pub.key}}" >> /home/$MY_USER/.ssh/authorized_keys
chmod 0600 /home/$MY_USER/.ssh/authorized_keys
chown -R $MY_USER:$MY_USER /home/$MY_USER/.ssh
chmod 0700 /home/$MY_USER/.ssh
echo "Create user $MY_USER done."

#install latest stable docker
apt-get -y install \
     apt-transport-https \
     ca-certificates \
     curl

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -

add-apt-repository \
            "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
       $(lsb_release -cs) \
       stable"

apt-get update
apt-get -y install docker-ce=17.03.1~ce-0~ubuntu-xenial
systemctl enable docker
systemctl start docker
echo "Install docker-ce='$(docker -v)' done."

#allow user to run docker without sudo
usermod -aG docker $MY_USER
echo "Add user $MY_USER in docker group"

echo "Complete user_data.sh ."

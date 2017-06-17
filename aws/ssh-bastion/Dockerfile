# prepare sshd & aws boto3 environment
FROM ubuntu:16.04

RUN apt-get -y update
RUN apt-get -y install openssh-server
RUN passwd -d root && mkdir -p /var/run/sshd

ARG MY_USER=dnikku
ADD .build /tmp/.build

# disable sshd PAM for not autologout after login
# disable sshd PasswordAuthentication and set unknown password for $MY_USER
RUN \
    sed -ri 's/UsePAM yes/UsePAM no/g' /etc/ssh/sshd_config && \
    sed -ri 's/\#PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config && \
    useradd -d /home/$MY_USER -m -s /bin/bash $MY_USER && \
    usermod -p "\$6\$!" $MY_USER && \
    mkdir -p /home/$MY_USER/.ssh && \
    cat /tmp/.build/id_rsa.pub >> /home/$MY_USER/.ssh/authorized_keys && \
    chown -R $MY_USER:$MY_USER /home/$MY_USER && \
    chmod -R 0700 /home/$MY_USER && \
    chmod 0600 /home/$MY_USER/.ssh/authorized_keys


EXPOSE 22
CMD ["/usr/sbin/sshd", "-D", "-e"]

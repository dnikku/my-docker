# prepare sshd & aws boto3 environment
FROM ubuntu:16.10

RUN apt-get -y update
RUN apt-get -y install openssh-server sudo less
RUN apt-get install -y net-tools iproute iptables ifupdown traceroute
RUN wget https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py && rm get-pip.py && \
    pip install boto3

#RUN rm -rf /var/lib/apt/lists/*
RUN passwd -d root && mkdir -p /var/run/sshd

ARG MY_USER=dnikku
ADD .build /tmp/.build

# disable sshd PAM for not autologout after login
# disable sshd PasswordAuthentication
# and set unknown password for $MY_USER, simulating unlocking user
RUN \
    sed -ri 's/UsePAM yes/UsePAM no/g' /etc/ssh/sshd_config && \
    sed -ri 's/\#PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config && \
    useradd -d /home/$MY_USER -m -s /bin/bash $MY_USER && \
    usermod -p "\$6\$*" $MY_USER && \
    mkdir -p /home/$MY_USER/.ssh && \
    cat /tmp/.build/id_rsa.pub >> /home/$MY_USER/.ssh/authorized_keys && \
    mv /tmp/.build/.aws /home/$MY_USER && \
    chown -R $MY_USER:$MY_USER /home/$MY_USER && \
    chmod -R 0700 /home/$MY_USER && \
    chmod 0600 /home/$MY_USER/.ssh/authorized_keys && \
    usermod -aG sudo $MY_USER && echo "$MY_USER ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers


# setup VPN over SSH using,
# see https://debian-administration.org/article/539/Setting_up_a_Layer_3_tunneling_VPN_with_using_OpenSSH
RUN \
    echo '\nPermitTunnel point-to-point\nPermitRootLogin forced-commands-only' >> /etc/ssh/sshd_config && \
    mkdir -p /root/.ssh && chmod 0700 /root/.ssh && \
    echo -n 'tunnel="0",command="ifdown tun0; ifup tun0" ' > /root/.ssh/authorized_keys && \
    cat /tmp/.build/id_rsa.pub >> /root/.ssh/authorized_keys && \
    chmod 0600 /root/.ssh/authorized_keys && \
    echo "\n\
iface tun0 inet static \n\
      address 10.254.254.1 \n\
      netmask 255.255.255.252 \n\
      pointopoint 10.254.254.2 \n\
      up iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE \n\
      up iptables -A FORWARD -i tun0 -o eth0 -j ACCEPT \n\
      up iptables -A FORWARD -i eth0 -o tun0 -m state --state RELATED,ESTABLISHED -j ACCEPT \n\
      post-down iptables -t nat --flush \n\
      post-down iptables --flush" >> /etc/network/interfaces


#EXPOSE 22
CMD ["/usr/sbin/sshd", "-D", "-e"]

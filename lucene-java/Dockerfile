FROM alpine:3.6

LABEL maintainer "https://github.com/dnikku"

ENV MY_USER=dnikku

RUN \
    # add edge repositories
    echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories && \
    echo "http://dl-2.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories && \
    apk add --update --no-cache bash util-linux procps dumb-init inetutils-syslogd && \
    echo "Welcome to Alpine: $(cat /etc/alpine-release)!" > /etc/motd && \
    mkdir -p /tmp/.build

# setup syslog
ADD alpine/syslog.conf /etc/syslog.conf

# setup ssh + create MY_USER
ADD alpine/ssh-setup.sh /tmp/.build
ADD alpine/sshd_config /tmp/.build
RUN /bin/sh /tmp/.build/ssh-setup.sh $MY_USER /tmp/.build/

# setup python3
ADD alpine/python3-setup.sh /tmp/.build
RUN /bin/sh /tmp/.build/python3-setup.sh

# setup java
ADD alpine/openjdk_1.8-setup.sh /tmp/.build
#RUN /build/oraclejdk_1.8-setup.sh
RUN /bin/sh /tmp/.build/openjdk_1.8-setup.sh


RUN rm -rf /var/cache/apk/* /tmp/.build

ENTRYPOINT ["/usr/bin/dumb-init", "--"]

#CMD ["bash", "-c", "do-some-pre-start-thing && exec my-server"]
CMD ["bash", "-c", "syslogd && exec /usr/sbin/sshd -D"]

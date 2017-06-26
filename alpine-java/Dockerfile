FROM alpine:3.6

LABEL maintainer "https://github.com/dnikku"

ENV MY_USER=dnikku

RUN \
    # add edge repositories
    echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories && \
    echo "http://dl-2.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories && \
    apk add --update --no-cache bash dumb-init inetutils-syslogd && \
    echo "Welcome to Alpine: $(cat /etc/alpine-release)!" > /etc/motd && \
    mkdir -p /tmp/.build

# syslog setup
ADD syslog.conf /etc/syslog.conf

# ssh setup + create MY_USER
ADD ssh /tmp/.build/ssh
RUN /bin/sh /tmp/.build/ssh/ssh-setup.sh $MY_USER /tmp/.build/ssh

# setup python3
ADD python /tmp/.build/python
RUN /bin/sh /tmp/.build/python/python3-setup.sh

# java setup
ADD java /tmp/.build/java
#RUN /build/oraclejdk_1.8-setup.sh
RUN /bin/sh /tmp/.build/java/openjdk_1.8-setup.sh

RUN rm -rf /var/cache/apk/* /tmp/.build

ENTRYPOINT ["/usr/bin/dumb-init", "--"]

#CMD ["bash", "-c", "do-some-pre-start-thing && exec my-server"]
CMD ["bash", "-c", "syslogd && exec /usr/sbin/sshd -D"]

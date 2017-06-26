FROM alpine:3.6

LABEL maintainer "https://github.com/dnikku"

RUN \
    apk add --update --no-cache bash && \
    echo "Welcome to Alpine: $(cat /etc/alpine-release)!" > /etc/motd

RUN rm /var/cache/apk/*

CMD ["bash"]

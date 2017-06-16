# prepare sshd & aws boto3 environment
FROM alpine

RUN \
 apk update && \
 apk add python3 && pip3 install --upgrade pip && pip3 install boto3 && \
 apk add openssh

ADD ./dnikku /home/dnikku
ADD ./my-boto3-init.sh /etc

RUN chmod +x /etc/my-boto3-init.sh && /etc/my-boto3-init.sh && rm /etc/my-boto3-init.sh

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D", "-f", "/etc/ssh/sshd_config"]

#!/bin/sh

cd /home/hellow

# forward request and error logs to docker log collector
mkdir -p /var/log/nginx
rm /var/log/ngingx/*.log
ln -sf /dev/stdout /var/log/nginx/access.log
ln -sf /dev/stderr /var/log/nginx/error.log

#start nginx as daemon
cp ./nginx.conf /etc/nginx/nginx.conf
nginx -c /etc/nginx/nginx.conf

#start supervisor
supervisord --nodaemon -c ./supervisord.ini

#!/bin/sh

cd /home/hellow

#start nginx as daemon
cp ./nginx.conf /etc/nginx/nginx.conf
nginx -c /etc/nginx/nginx.conf

#start supervisor
supervisord --nodaemon -c ./supervisord.ini

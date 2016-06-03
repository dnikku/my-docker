#!/bin/sh

cd /home/hellow

#start nginx as daemon
cp ./nginx.conf /etc/nginx/nginx.conf
nginx -c /etc/nginx/nginx.conf

#start supervisor
#supervisord -c /home/oa2b/supervisord.conf
gunicorn -w 1 -b 127.0.0.1:8001 flask_app:app

# prepare nginx, python, flask environment
FROM alpine


# manual get o copy from: https://bootstrap.pypa.io/get-pip.py
#  to avoid install curl/wget
ADD ./get-pip.py /

RUN apk update && apk add python nginx \
    && python get-pip.py && rm /get-pip.py \
    && pip install flask supervisor gunicorn

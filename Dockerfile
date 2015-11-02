# Docker image for Drone's HipChat notification plugin
#
#     docker build --rm=true -t plugins/drone-hipchat .

FROM gliderlabs/alpine:3.2
MAINTAINER Greg Taylor <gtaylor@gc-taylor.com>

RUN apk-install python3
RUN mkdir -p /usr/src/drone-hipchat
WORKDIR /usr/src/drone-hipchat

COPY requirements.txt /usr/src/drone-hipchat/
RUN pip3 install -r requirements.txt

COPY send-notification.py /usr/src/drone-hipchat/

ENTRYPOINT ["python3", "send-notification.py"]

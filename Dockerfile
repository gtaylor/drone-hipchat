# Docker image for Drone's HipChat notification plugin
#
#     docker build --rm=true -t plugins/drone-hipchat .

FROM python:3.5
MAINTAINER Greg Taylor <gtaylor@gc-taylor.com>

RUN mkdir /usr/src/drone-hipchat
WORKDIR /usr/src/drone-hipchat

COPY requirements.txt /usr/src/drone-hipchat/
RUN pip install -r requirements.txt

COPY send-notification.py /usr/src/drone-hipchat/

ENTRYPOINT ["./send-notification.py"]

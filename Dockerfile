FROM python:latest
MAINTAINER Toni Pesola

ADD /datalogger/requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

WORKDIR /app

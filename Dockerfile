FROM python:latest
MAINTAINER Toni Pesola

COPY datalogger /datalogger

RUN pip install -r /datalogger/requirements.txt

WORKDIR /datalogger

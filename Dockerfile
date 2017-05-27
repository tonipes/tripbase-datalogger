FROM python:latest
MAINTAINER Toni Pesola

ARG GIT_COMMIT_SHA=0
ARG GIT_COMMIT_TAG=0

COPY datalogger /datalogger

RUN pip install -r /datalogger/requirements.txt

WORKDIR /datalogger

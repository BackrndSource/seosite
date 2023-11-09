# syntax=docker/dockerfile:1.4

FROM python:3.9.18-alpine AS builder
WORKDIR /app 
COPY ./seosite /app

RUN apk add --virtual build-deps gcc musl-dev \
    && apk add --no-cache mariadb-dev

RUN pip install -r requirements.txt --no-cache-dir

RUN apk del build-deps

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"] 

#!/usr/bin/env bash
DJANGO_SETTINGS_MODULE=myproject.settings.dev \
DJANGO_SECRET_KEY="change-this-to-50-characters-long-random-string" \
DATABASE_NAME=myproject \
DATABASE_USER=myproject \
DATABASE_PASSWORD="change-this-too" \
EMAIL_HOST="localhost" \
EMAIL_PORT="25" \
EMAIL_HOST_USER="" \
EMAIL_HOST_PASSWORD="" \
PIP_REQUIREMENTS=dev.txt \
docker-compose up --detach --build

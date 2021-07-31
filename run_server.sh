#!/bin/bash

if [ "$1" = "prod" ];
then
    echo "Running using production settings"
    export DJANGO_SETTINGS_MODULE="config.production_settings"
else
    echo "Running using local settings"
    export DJANGO_SETTINGS_MODULE="config.local_settings"
fi

./manage.py runserver

#!/bin/bash

# Start scrapyd process
(cd scrapy_app/ && scrapyd &)

# Start django server
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?

#!/bin/sh
python ./manage.py migrate
python ./manage.py loaddata /app/data/polls-v4.json /app/data/votes-v4.json /app/data/users.json
python ./manage.py runserver 0.0.0.0:8000
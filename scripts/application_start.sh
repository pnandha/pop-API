#!/bin/bash
cd /home/ubuntu/pop-API
source env/bin/activate

cd /home/ubuntu/pop-API/backend

#python3 manage.py migrate
python3 manage.py collectstatic --noinput

gunicorn -c Config/gunicorn/dev.py

sudo service nginx restart
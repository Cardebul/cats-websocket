#!/bin/bash
cd /app

python manage.py collectstatic --noinput

python manage.py makemigrations 
python manage.py migrate

echo "-----------GOOOOOOOD--------- "

# echo "-----------Run daphne local server--------- "

# python -m daphne -b 0.0.0.0 -p 8001 kittygram_backend.asgi:application

# echo "-----------Run gunicorn local server--------- "

# python -m gunicorn --bind 0.0.0.0:8000 kittygram_backend.wsgi

#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Create the admin user if it doesn't exist
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='alaye').exists():
    User.objects.create_superuser('alaye', '', '123')
    print('Created admin user: alaye')
else:
    print('Admin user alaye already exists')
"
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Always create or reset the admin user (idempotent, safe to run every deploy)
python manage.py shell -c "
from django.contrib.auth.models import User
user, created = User.objects.get_or_create(username='alaye')
user.set_password('123')
user.is_staff = True
user.is_superuser = True
user.save()
print('Admin user alaye: password set to 123 (created=' + str(created) + ')')
"
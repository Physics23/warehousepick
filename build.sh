#!/usr/bin/env bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Create the admin user (idempotent)
python manage.py shell -c "
from django.contrib.auth.models import User
user, _ = User.objects.get_or_create(username='alaye')
user.set_password('123')
user.is_staff = True
user.is_superuser = True
user.save()
print('Admin user alaye ready')
"

# Create the station and totes (idempotent)
python manage.py shell -c "
from picks.models import Station, Tote
s, c1 = Station.objects.get_or_create(station_id='ToteASRS4159', defaults={'name': 'Pick Station'})
t1, c2 = Tote.objects.get_or_create(tote_id='BIN-01')
t2, c3 = Tote.objects.get_or_create(tote_id='TOTE-42')
print(f'Station ToteASRS4159: {\"created\" if c1 else \"exists\"}')
print(f'Totes BIN-01/TOTE-42: {\"created\" if c2 else \"exists\"}/{\"created\" if c3 else \"exists\"}')
"
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from picks.models import Station, Item, Tote, PickSession, PickTask
import random

class Command(BaseCommand):
    help = 'Generates a continuous loop of 20 NEW items and tasks every time you run it'

    def handle(self, *args, **kwargs):
        # 1. Create a default user (or find existing one)
        if not User.objects.filter(username='admin').exists():
            User.objects.create_user(username='admin', password='123')
            self.stdout.write(self.style.SUCCESS('Created user: alaye (password: 123)'))
        else:
            self.stdout.write(self.style.WARNING('User alaye already exists'))

        # 2. Get the existing station or create it
        station, _ = Station.objects.get_or_create(station_id='ToteASRS4159', name='Main Pick Station')

        # 3. Get or create the totes
        source_tote, _ = Tote.objects.get_or_create(tote_id='BIN-01')
        dest_tote, _ = Tote.objects.get_or_create(tote_id='TOTE-42')

        # 4. Create active session (or renew it)
        session, _ = PickSession.objects.get_or_create(
            station=station,
            operator_name='alaye',
            is_active=True,
            defaults={'start_time': timezone.now()}
        )

        # 5. Get a random number to create unique SKUs (so we don't repeat)
        random_id = random.randint(1000, 9999)

        # 6. Create 20 new items with UNIQUE SKUs
        items = []
        for i in range(1, 21):
            sku = f'LOOP-{random_id}-{i:04d}'
            item, _ = Item.objects.get_or_create(
                sku=sku,
                defaults={
                    'name': f'Loop Item {i}',
                    'description': f'Auto-generated loop item for continuous demo. SKU: {sku}',
                    'image': '',
                }
            )
            items.append(item)

        # 7. Create 20 new pending tasks
        tasks_created = 0
        for item in items:
            task, created = PickTask.objects.get_or_create(
                session=session,
                item=item,
                source_tote=source_tote,
                destination_tote=dest_tote,
                defaults={'status': PickTask.Status.PENDING}
            )
            if created:
                tasks_created += 1

        self.stdout.write(self.style.SUCCESS(f'Created {tasks_created} new pending tasks!'))
        self.stdout.write(self.style.SUCCESS('SEEDING COMPLETE! ✅'))
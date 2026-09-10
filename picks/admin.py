from django.contrib import admin
from .models import Station, Item, Tote, PickSession, PickTask

admin.site.register(Station)
admin.site.register(Item)
admin.site.register(Tote)
admin.site.register(PickSession)
admin.site.register(PickTask)

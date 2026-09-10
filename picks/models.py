from django.db import models
from django.utils import timezone

class Station(models.Model):
    station_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.station_id

class Item(models.Model):
    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.URLField(max_length=500, blank=True, null=True)  # Stores URLs (picsum)

    def __str__(self):
        return f"{self.sku} - {self.name}"

class Tote(models.Model):
    tote_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tote_id

class PickSession(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='sessions')
    operator_name = models.CharField(max_length=100)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Session {self.id} @ {self.station.station_id}"

class PickTask(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PICKED = 'picked', 'Picked'
        UNSCANNABLE = 'unscannable', 'Unscannable'
        MISSING = 'missing', 'Missing'
        PROBLEM_TOTE = 'problem_tote', 'Problem Tote'

    session = models.ForeignKey(PickSession, on_delete=models.CASCADE, related_name='tasks')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    source_tote = models.ForeignKey(Tote, on_delete=models.CASCADE, related_name='source_tasks')
    destination_tote = models.ForeignKey(Tote, on_delete=models.CASCADE, related_name='destination_tasks')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    picked_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Task {self.id}: {self.item.sku} ({self.status})"
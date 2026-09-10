from rest_framework import serializers
from .models import Station, Item, Tote, PickSession, PickTask

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'sku', 'name', 'description', 'image']

class ToteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tote
        fields = ['id', 'tote_id']

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ['id', 'station_id', 'name']

class PickSessionSerializer(serializers.ModelSerializer):
    station = StationSerializer(read_only=True)
    class Meta:
        model = PickSession
        fields = ['id', 'station', 'operator_name', 'start_time', 'end_time', 'is_active']

class PickTaskSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    source_tote = ToteSerializer(read_only=True)
    destination_tote = ToteSerializer(read_only=True)
    session = PickSessionSerializer(read_only=True)

    class Meta:
        model = PickTask
        fields = ['id', 'session', 'item', 'source_tote', 'destination_tote', 'status', 'picked_at']

class StationStatsSerializer(serializers.Serializer):
    rate_uph = serializers.FloatField()
    cycle_time_secs = serializers.FloatField()
    session_time_secs = serializers.FloatField()
    total_units_picked = serializers.IntegerField()
    operator_name = serializers.CharField()
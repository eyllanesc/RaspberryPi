from rest_framework import serializers

from Domo.models import Sensor


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ('date_created', 'temperature', 'humidity')

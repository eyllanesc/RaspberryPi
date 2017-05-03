from rest_framework import serializers

from Domo.models import Sensor, Motor


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ('date_created', 'temperature', 'humidity')


class MotorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motor
        fields = ('date_created', 'status')
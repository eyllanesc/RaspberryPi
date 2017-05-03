from django.shortcuts import render
from rest_framework import viewsets

from Domo.models import Sensor, Motor
from Domo.serializers import SensorSerializer, MotorSerializer


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all().order_by('-id')[:40]
    serializer_class = SensorSerializer


class MotorViewSet(viewsets.ModelViewSet):
    queryset = Motor.objects.all()
    serializer_class = MotorSerializer


def home(request):
    return render(request, 'index.html')

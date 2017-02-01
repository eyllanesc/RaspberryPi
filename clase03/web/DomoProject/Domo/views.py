from django.shortcuts import render
from rest_framework import viewsets

from Domo.models import Sensor
from Domo.serializers import SensorSerializer


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all().order_by('-id')[:40]
    serializer_class = SensorSerializer


def home(request):
    return render(request, 'index.html')

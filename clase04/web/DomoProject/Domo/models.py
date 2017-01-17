from __future__ import unicode_literals

from django.db import models


class Sensor(models.Model):
    date_created = models.DateTimeField(auto_now=True)
    temperature = models.FloatField()
    humidity = models.FloatField()

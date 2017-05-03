from django.contrib import admin

from Domo.models import Sensor, Motor


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('date_created', 'temperature', 'humidity')


@admin.register(Motor)
class MotorAdmin(admin.ModelAdmin):
    list_display = ('date_created', 'status')

class Motor(models.Model):
	date_created = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=40)

serializers.py:


from Domo.models import Sensor, Motor

class MotorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motor
        fields = ('date_created', 'status')

views.py:


from Domo.models import Sensor, Motor
from Domo.serializers import SensorSerializer, MotorSerializer

class MotorViewSet(viewsets.ModelViewSet):
    queryset = Motor.objects.all()
    serializer_class = MotorSerializer

admin.py

from Domo.models import Sensor, Motor


@admin.register(motor)
class MotorAdmin(admin.ModelAdmin):
    list_display = ('date_created', 'status')


urls.py 
from Domo.views import SensorViewSet, MotorViewSet

router.register(r'sensors', SensorViewSet)
router.register(r'motors', MotorViewSet)
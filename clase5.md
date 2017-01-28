models.py

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
	
	
	
index.html

	var state = "stop";
	
	 function myFunction() {
	
	    $.ajax({
	                url: "/api/motors/", // the endpoint
	                type: "POST", // http method
	                // handle a successful response
	                success: function (data) {
	                    state = !state;
	                    console.log(data);
	                    console.log(state);
	                },
	                data: {
	                    'date_created': new Date(),
	                    'state': state
	                },
	                // handle a non-successful response
	                error: function (xhr, errmsg, err) {
	
	                }
	            });
	    }
	    
En el mismo index.html:

	<div style="text-align:center;margin:auto;">
	    <button onclick="myFunction()">Toggle</button>
	</div>
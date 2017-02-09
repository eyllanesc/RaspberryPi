### Configuración de motion

Creamos un directorio para guardar las imagenes:

```bash
pi@raspberrypi:~ $ mkdir  /home/pi/Monitor
pi@raspberrypi:~ $ sudo chgrp motion /home/pi/Monitor
pi@raspberrypi:~ $ sudo chmod g+rwx /home/pi/Monitor
pi@raspberrypi:~ $ sudo chmod -R g+w /home/pi/Monitor/
```
Instalamos la librería **motion**.

```bash
pi@raspberrypi:~ $ sudo apt-get install -y motion
```
Editamos el archivo motion.conf, buscando los siguientes campos y los cambiamos a lo siguientes valores:

```bash
pi@raspberrypi:~ $ sudo nano /etc/motion/motion.conf
```
	stream_localhost off
	webcontrol_localhost off
	framerate 60
	target_dir /home/pi/Monitor
	
	
Editamos el archivo **/etc/default/motion** y cambiamos de **no** a **yes**

```bash
pi@raspberrypi:~ $ sudo nano /etc/default/motion
```
	start_motion_daemon=yes

Despues ejecutamos lo siguiente:

	pi@raspberrypi:~ $ sudo service motion stop
	pi@raspberrypi:~ $ sudo service motion start
	
Y Accedemos a la imagen de la cámara a traves de la url desde nuestro buscador: http://{your-rpi-address}:8081/ 

Obteniendo lo siguiente:

![](imagenes/Screenshot.png) 


Las imagenes y videos pueden llenar el almacenamiento, por ello configuramos que pasada los 15 minutos despues de cada hora borre todos excepto las 20 ultimas imagenes:

```bash
pi@raspberrypi:~ $ sudo crontab -e
```


	15 * * * * (date; ls /home/pi/Monitor/*.jpg | head -n -20 | xargs rm -v) >> /tmp/images_deleted 2>&1


### Configurando el Servidor

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

	
	
	 function myFunction(state) {
	
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
	    
	    function forward(){
	    	myFunction("fordward");
	    }
	    
En el mismo index.html:

	<div style="text-align:center;margin:auto;">
	    <button onclick="forward()">Avanzar</button>
	</div>
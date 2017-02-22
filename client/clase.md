##Clientes

### Python

#### GET method:

```python
import requests
import datetime

url = 'http://192.168.2.9/api/sensors/'

response = requests.get(url)
assert response.status_code == 200

for data in response.json():
    date = datetime.datetime.strptime(data['date_created'][:-1], "%Y-%m-%dT%H:%M:%S.%f")
    humidity = data['humidity']
    temperature = data['temperature']
    print("Fecha: {}, Humedad: {}, Temperatura: {}".format(date, humidity, temperature))
    
```

#### POST method:

```python
import requests
import datetime
import json
import time

url = 'http://192.168.2.9/api/sensors/'

 for i in range(100):
	date = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')

	headers = {'Content-type': 'application/json'}
	response = requests.post(url,  data =json.dumps({'date_created': date,'temperature': 11.1, 'humidity': 10.1}), headers=headers)
	assert response.status_code == 201
	time.sleep(0.1)
	
```

### ESP8266

Para realizar esta parte es necesario tener instalado las herramientas necesarias para compilar y quemar el *ESP8266*

#### esp8266-restclient [link](https://github.com/csquared/arduino-restclient) 

```console
cd ~/Documents/Arduino
mkdir libraries
cd libraries
git clone https://github.com/dakaz/esp8266-restclient.git RestClient
```

#### SimpleDHT [link](https://github.com/winlinvip/SimpleDHT)

```console
cd ~/Documents/Arduino
mkdir libraries
cd libraries
git clone https://github.com/winlinvip/SimpleDHT.git SimpleDHT
```

Código del cliente:

```cpp
#include <RestClient.h>
#include <ESP8266WiFi.h>
#include <SimpleDHT.h>


const char* ssid     = "{your ssid}";
const char* password = "{your password}";

const char* host = "{your ip or domain}";

RestClient client = RestClient(host);

int pinDHT11 = 2;
SimpleDHT11 dht11;

void setup() {
    Serial.begin(115200);
    delay(10);
    client.setContentType("application/json");
    // We start by connecting to a WiFi network
    
    Serial.println();
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);
    
    /* Explicitly set the ESP8266 to be a WiFi-client, otherwise, it by default,
     would try to act as both a client and an access-point and could cause
     network-issues with your other WiFi-devices on your WiFi-network. */
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    
    Serial.println("");
    Serial.println("WiFi connected");  
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
}

String response;
char buffer[50];
void loop(){
    byte temperature = 0;
    byte humidity = 0;
    if (dht11.read(pinDHT11, &temperature, &humidity, NULL)) {
        Serial.print("Read DHT11 failed.");
        return;
    }
    
    response = "";
    sprintf (buffer, "{\"temperature\": %d, \"humidity\": %d}",(int)temperature, (int)humidity);
    int statusCode = client.post("/api/sensors/", buffer , &response);
    if(statusCode == 201){;
        Serial.println(response);
    }
    delay(2000);
}
```


### Configuración de motion

Creamos un directorio para guardar las imagenes:

```console
pi@raspberrypi:~ $ mkdir  /home/pi/Monitor
pi@raspberrypi:~ $ sudo chgrp motion /home/pi/Monitor
pi@raspberrypi:~ $ sudo chmod g+rwx /home/pi/Monitor
pi@raspberrypi:~ $ sudo chmod -R g+w /home/pi/Monitor/
```
Instalamos la librería **motion**.

```console
pi@raspberrypi:~ $ sudo apt-get install -y motion
```
Editamos el archivo motion.conf, buscando los siguientes campos y los cambiamos a lo siguientes valores:

```console
pi@raspberrypi:~ $ sudo nano /etc/motion/motion.conf
```

	stream_localhost off
	webcontrol_localhost off
	framerate 60
	target_dir /home/pi/Monitor

	
Editamos el archivo **/etc/default/motion** y cambiamos de **no** a **yes**

```console
pi@raspberrypi:~ $ sudo nano /etc/default/motion
```
	start_motion_daemon=yes

Despues ejecutamos lo siguiente:

```console
pi@raspberrypi:~ $ sudo service motion stop
pi@raspberrypi:~ $ sudo service motion start
```
	
Y Accedemos a la imagen de la cámara a traves de la url desde nuestro buscador: http://{your-rpi-address}:8081/ 

Obteniendo lo siguiente:

![](imagenes/Screenshot.png) 


Las imagenes y videos pueden llenar el almacenamiento, por ello configuramos que pasada los 15 minutos despues de cada hora borre todos excepto las 20 ultimas imagenes:

```console
pi@raspberrypi:~ $ sudo crontab -e
```


	15 * * * * (date; ls /home/pi/Monitor/*.jpg | head -n -20 | xargs rm -v) >> /tmp/images_deleted 2>&1


### Configurando el Servidor


Implementamos el servidor para que provea y guarde los datos, para ellos creamos el modelo Motor que contiene 2 atributos: *date_created* que guarda la fecha de creación del comando y *status* que contiene el comando respectivo. Además de los serializers y vistas respectivas.

##### Domo/models.py

```python
from __future__ import unicode_literals

from django.db import models

STATUS_CHOICES = (
    ('F', 'Forward'),
    ('B', 'Backward'),
    ('L', 'Left'),
    ('R', 'Right'),
    ('S', 'Stop')
)

# Create your models here.

class Motor(models.Model):
    date_created = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='S')

```
##### Domo/serializers.py:

```python	

from rest_framework import serializers

from Domo.models import Motor

class MotorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motor
        fields = ('date_created', 'status')

```	

##### Domo/views.py:

```python
from django.shortcuts import render
from rest_framework import viewsets

# Create your views here.
from Domo.models import Motor
from Domo.serializers import MotorSerializer

class MotorViewSet(viewsets.ModelViewSet):
    queryset = Motor.objects.all()
    serializer_class = MotorSerializer
```
	
##### Domo/admin.py

```python
from django.contrib import admin
from Domo.models import Motor

# Register your models here.
@admin.register(Motor)
class MotorAdmin(admin.ModelAdmin):
    list_display = ('date_created', 'status')
```
	

##### Domo/urls.py 

```python
from rest_framework import routers
from Domo.views import MotorViewSet

router = routers.DefaultRouter()
router.register(r'motors', MotorViewSet)

urlpatterns = router.urls
```

Creamos el archivo index.html donde implementamos las peticiones mediante javascript utilizando ajax.
	
##### templates/index.html

	
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Proyecto</title>
</head>

<body>

<div style="text-align:center;margin:auto;">
    <button onclick="forward()">Avanzar</button>
</div>

<div style="text-align:center;margin:auto;">
    <button onclick="backward()">Retroceder</button>
</div>

<div style="text-align:center;margin:auto;">
    <button onclick="left()">Izquierda</button>
</div>

<div style="text-align:center;margin:auto;">
    <button onclick="right()">Derecha</button>
</div>

<div style="text-align:center;margin:auto;">
    <button onclick="stop()">Parar</button>
</div>

<img id="ip_link" src="" target="_blank" />

</body>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/2.0.0/jquery.min.js"></script>
<script type="text/javascript">

    var ip = location.host;
    document.getElementById("ip_link").src = "http://"+ip+":8081";

    // Load all posts on page load
    function move(state) {
        $.ajax({
            url: "/api/motors/", // the endpoint
            type: "POST", // http method
            // handle a successful response
            success: function (data) {

	        },
            data: {
               	'date_created': new Date(),
                'status': state
            },
            // handle a non-successful response
            error: function (xhr, errmsg, err) {

                }
            });

        };

    function forward(){
    	move('F');
    };

    function backward(){
    	move('B');
    };

    function left(){
    	move('L');
    };

    function right(){
    	move('R');
    };

    function stop(){
    	move('S');
    };

</script>
</html>
```

Obteniendo algo similar a la siguiente imagen:

![](imagenes/Proyecto.png) 

Luego implementamos la clase **Car**  que se encarga de manejar los movimientos del vehículo.

##### Car.py

```python
import RPi.GPIO as GPIO
import time


class Car:
    def __init__(self, motorL, motorR):
        """
        Manejar los motores
        :param pins:
        [in1, in2, in3, in4]
        """
        GPIO.setmode(GPIO.BCM)
        self._pinsA = motorL
        self._pinsB = motorR

        for pin in (self._pinsA + self._pinsB):
            GPIO.setup(pin, GPIO.OUT)

    def motorOn(self, pins):
        GPIO.output(pins[0], False)
        GPIO.output(pins[1], True)

    def motorOff(self, pins):
        GPIO.output(pins[0], False)
        GPIO.output(pins[1], False)

    def motorReverse(self, pins):
        GPIO.output(pins[0], True)
        GPIO.output(pins[1], False)

    def forward(self):
        self.stop()
        self.motorOn(self._pinsA)
        self.motorOn(self._pinsB)
        time.sleep(0.2)
        self.stop()

    def backward(self):
        self.stop()
        self.motorReverse(self._pinsA)
        self.motorReverse(self._pinsB)
        time.sleep(0.2)
        self.stop()

    def left(self):
        self.stop()
        self.motorOn(self._pinsB)
        self.motorReverse(self._pinsA)
        time.sleep(0.2)
        self.stop()

    def right(self):
        self.stop()
        self.motorOn(self._pinsA)
        self.motorReverse(self._pinsB)
        time.sleep(0.2)
        self.stop()

    def stop(self):
        self.motorOff(self._pinsA)
        self.motorOff(self._pinsB)

    def __exit__(self, exc_type, exc_val, exc_tb):
        GPIO.cleanup()
```


Ahora creamos la clase **Data** que se encarga de obtener los datos, filtrar el último y verificar si este ha sido creado en menos de 1 segundo. Si cumple lo anterior obtenemos el comando  **status** y realizamos la tarea respectiva.

##### main.py

```python
from datetime import datetime, timedelta
from Car import Car
import requests


class Data:
    def __init__(self, url, timeout=1):
        self.url = url
        self.before = None
        self.timeout = timeout

    def load(self):
        response = requests.get(self.url)
        assert response.status_code == 200
        data = response.json()[-1]
        date = datetime.strptime(data['date_created'][:-1], "%Y-%m-%dT%H:%M:%S.%f")
        if self.before == date:
            return
        self.before = date
        u = datetime.utcnow()
        diff = u - date
        if diff < timedelta(seconds=self.timeout):
            return data['status']

if __name__ == '__main__':
    data = Data(url='http://192.168.2.10/api/motors/')
    motorL = [17, 27]
    motorR = [23, 24]

    car = Car(motorL, motorR)

    while True:
        resp = data.load()
        if resp == 'F':
            car.forward()
        elif resp == 'B':
            car.backward()
        elif resp == 'L':
            car.left()
        elif resp == 'R':
            car.right()
        elif resp == 'S':
            car.stop()
```

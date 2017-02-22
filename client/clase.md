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

### Robot Móvil:

Luego implementamos la clase **Car**  que se encarga de manejar los movimientos del vehículo.

##### Car.py

```python
import RPi.GPIO as GPIO
import time


class Car:
    def __init__(self, motorL, motorR, t=0.2):
        """
        Manejar los motores
        :param pins:
        [in1, in2, in3, in4]
        """
        GPIO.setmode(GPIO.BCM)
        self._pinsA = motorL
        self._pinsB = motorR
        self.t = t 

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
        time.sleep(self.t)
        self.stop()

    def backward(self):
        self.stop()
        self.motorReverse(self._pinsA)
        self.motorReverse(self._pinsB)
        time.sleep(self.t)
        self.stop()

    def left(self):
        self.stop()
        self.motorOn(self._pinsB)
        self.motorReverse(self._pinsA)
        time.sleep(self.t)
        self.stop()

    def right(self):
        self.stop()
        self.motorOn(self._pinsA)
        self.motorReverse(self._pinsB)
        time.sleep(self.t)
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
#!/usr/bin/env python
from datetime import datetime, timedelta
from Car import Car
import requests
import RPi.GPIO as GPIO
import socket

class Data:
    def __init__(self, url, timeout=1):
        self.url = url
        self.before = None
        self.timeout = timeout

    def load(self):
        response = requests.get(self.url)
        s = response.headers['date']
        u = datetime.strptime(s, "%a, %d %b %Y %H:%M:%S %Z")
        assert response.status_code == 200
        data = response.json()[0]
        date = datetime.strptime(data['date_created'][:-1], "%Y-%m-%dT%H:%M:%S.%f")
        if self.before == date:
            return
        self.before = date
        # u = datetime.utcnow()
        diff = u - date
        if diff < timedelta(seconds=1.5):
            return data['status']


#http://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 0))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


if __name__ == '__main__':
    host = get_ip()
    print(host)
    data = Data(url='http://'+host+'/api/motors/')
    motorL = [17, 27]
    motorR = [23, 24]
    car = Car(motorL, motorR, 1)

    while True:
        try:
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
        except (KeyboardInterrupt, SystemExit):
	       GPIO.cleanup()
	    break
```

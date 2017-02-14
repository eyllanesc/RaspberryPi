###Car.py

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

###bluecarpy.py

```python
from bluetooth import *
from Car import Car

import os

os.system("sudo hciconfig hci0 name \'raspberrypi-0\'")

os.system("sudo hciconfig hci0 piscan")

server_sock = BluetoothSocket(RFCOMM)
server_sock.bind(("", PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service(server_sock, "AquaPiServer",
                  service_id=uuid,
                  service_classes=[uuid, SERIAL_PORT_CLASS],
                  profiles=[SERIAL_PORT_PROFILE],
                  #                   protocols = [ OBEX_UUID ]
                  )
motorL = [17, 27]
motorR = [23, 24]

car = Car(motorL, motorR)

while True:
    print "Waiting for connection on RFCOMM channel %d" % port

    client_sock, client_info = server_sock.accept()
    print "Accepted connection from ", client_info

    try:
        data = client_sock.recv(1024)
        if len(data) == 0:
            break

        if data == 'Forward':
            car.forward()
        elif data == 'Backward':
            car.backward()
        elif data == 'Left':
            car.left()
        elif data == 'Right':
            car.right()
        elif data == 'Stop':
            car.stop()
        else:
            data = 'ERROR'
        data += "!"
        client_sock.send(data)
    except IOError:
        pass

    except KeyboardInterrupt:
        client_sock.close()
        server_sock.close()
        break
```

Añadir permiso para poder acceder al recurso de ***Bluetooth***.

###AndroidManifest.xml

```xml
....
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
package="com.rpi.bluecarpi.bluecarpi">
<uses-permission android:name="android.permission.BLUETOOTH" />
<application
...
```

### MainActivity.java

```java
public class MainActivity extends AppCompatActivity {

    BluetoothSocket _Socket;
    BluetoothDevice _Device = null;

    final byte delimiter = 33;
    int readBufferPosition = 0;

    public void sendBtMsg(String msg){
        UUID uuid = UUID.fromString("94f39d29-7d6d-437d-973b-fba39e49d4ee"); //Standard SerialPortService ID
        try {

            _Socket = _Device.createRfcommSocketToServiceRecord(uuid);
            if (!_Socket.isConnected()){
                _Socket.connect();
            }

            OutputStream mmOutputStream = _Socket.getOutputStream();
            mmOutputStream.write(msg.getBytes());

        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        final Handler handler = new Handler();

        final Button btnBackward = (Button)findViewById(R.id.btnBackward);
        final Button btnForward = (Button)findViewById(R.id.btnForward);
        final Button btnLeft = (Button)findViewById(R.id.btnLeft);
        final Button btnRight = (Button)findViewById(R.id.btnRight);
        final Button btnStop = (Button)findViewById(R.id.btnStop);

        final BluetoothAdapter _bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();

        final class workerThread implements Runnable{

            private String btMsg;

            public workerThread(String msg){
                btMsg = msg;
            }

            @Override
            public void run() {
                sendBtMsg(btMsg);

                while (!Thread.currentThread().isInterrupted()){
                    int bytesAvailable;

                    boolean workDone = false;
                    try {

                        final InputStream _inputStream;
                        _inputStream = _Socket.getInputStream();

                        bytesAvailable = _inputStream.available();

                        if(bytesAvailable>0){
                            byte[] packetBytes = new byte[bytesAvailable];
                            byte[] readBuffer = new byte[1024];
                            _inputStream.read(packetBytes);

                            for(int i=0; i<bytesAvailable; i++){
                                byte b=packetBytes[i];
                                if(b==delimiter){
                                    byte[] encodedBytes = new byte[readBufferPosition];
                                    System.arraycopy(readBuffer, 0, encodedBytes, 0, encodedBytes.length);
                                    final String data = new String(encodedBytes, "US-ASCII");
                                    readBufferPosition = 0;
                                    handler.post(new Runnable() {
                                        @Override
                                        public void run() {

                                        }
                                    });
                                    workDone = true;
                                    break;
                                }
                                else {
                                    readBuffer[readBufferPosition++] = b;
                                }
                            }

                            if(workDone){
                                _Socket.close();
                                break;
                            }
                        }
                    }
                    catch (IOException e){
                        e.printStackTrace();
                    }
                }

            }
        }


        assert btnForward != null;
        btnForward.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                (new Thread(new workerThread("Forward"))).start();
            }
        });

        assert btnBackward != null;
        btnBackward.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                (new Thread(new workerThread("Backward"))).start();
            }
        });

        assert btnLeft != null;
        btnLeft.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                (new Thread(new workerThread("Left"))).start();
            }
        });

        assert btnRight != null;
        btnRight.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                (new Thread(new workerThread("Right"))).start();
            }
        });

        assert btnStop != null;
        btnStop.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                (new Thread(new workerThread("Stop"))).start();
            }
        });

        if(!_bluetoothAdapter.isEnabled()){
            Intent enableBluetooth = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivityForResult(enableBluetooth, 0);
        }

        Set<BluetoothDevice> pairedDevice = _bluetoothAdapter.getBondedDevices();

        if(pairedDevice.size() > 0){
            for (BluetoothDevice device:pairedDevice){
                if(device.getName().equals("raspberrypi-0")){
                    _Device = device;
                }
            }
        }
    }


}
```
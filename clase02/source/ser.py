#!/usr/bin/env python
import serial # Importamos la libreria serial para manejar el puerto serial
ser = serial.Serial('/dev/ttyAMA0', 9600)# puerto+baudio
ser.write('some text') # Envia el String
while True:
    print(ser.read()) #lee la respuesta

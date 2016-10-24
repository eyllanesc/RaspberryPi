#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
#pines en nomenclatura BCM para hacer la conexion del Rpi
rows = [17, 25, 24, 23]
cols = [27, 18, 22]
#Valores del teclado 
keys = [	
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['*', '0', '#']]
for row_pin in rows:
    GPIO.setup(row_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #configuracion de pines como entrada
for col_pin in cols:
    GPIO.setup(col_pin, GPIO.OUT)	#configuracion de pines como salida
def get_key():
    key = 0
    for col_num, col_pin in enumerate(cols):
        GPIO.output(col_pin, 1) #habilita una fila
        for row_num, row_pin in enumerate(rows):
            if GPIO.input(row_pin):#chequea si un boton del teclado ha sido presionado
                key = keys[row_num][col_num] # obtiene el valor del teclado
        GPIO.output(col_pin, 0)
    return key
while True:
    key = get_key()#usa la función "key" para obtener el caracter apretado
    if key :
        print(key)#imprime el valor rescatado
    time.sleep(0.3)

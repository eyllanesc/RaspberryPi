#!/usr/bin/env python
import RPi.GPIO as GPIO #import GPIO library
import time #import time for managed time
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)#GPIO 18 como entrada
while True:
    input_state = GPIO.input(18) #leemos la entrada
    if input_state == False: #si esta en nivel bajo
	print('Button Pressed') #imprime esto
    time.sleep(0.2) #tiempo muerto

#!/usr/bin/python
import RPi.GPIO as GPIO
import time
led = 18  #GPIO18
delay = 1 #one second
GPIO.setwarnings(False) #disable warnings
GPIO.setmode(GPIO.BCM) # mode BCM or Board
GPIO.setup(led, GPIO.OUT) # input or output
isRunning = True
while isRunning:
	try:
		GPIO.output(led, True)
		time.sleep(delay)
		GPIO.output(led, False)
		time.sleep(delay)
	except KeyboardInterrupt:
		isRunning = False
GPIO.cleanup()
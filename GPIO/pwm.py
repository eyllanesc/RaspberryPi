#!/usr/bin/python
import RPi.GPIO as GPIO
led = 18  #GPIO18
GPIO.setwarnings(False) #disable warnings
GPIO.setmode(GPIO.BCM) # mode BCM or Board
GPIO.setup(led, GPIO.OUT) # input or output
pwm_led = GPIO.PWM(led, 500)
pwm_led.start(100)
isRunning = True
while isRunning:
	try:
		duty_s = raw_input("Enter Brightness (0 to 100): ")
		duty = int(duty_s)
		pwm_led.ChangeDutyCycle(duty)
	except KeyboardInterrupt:
		isRunning = False
GPIO.cleanup()
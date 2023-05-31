#-*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

button_pin = 15 #GPIO 4

GPIO.setwarnings(False) #remove warning

GPIO.setmode(GPIO.BCM) #set mode of GPIO as BCM

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #set led in/out

while 1:
    if GPIO.input(button_pin) == GPIO.HIGH:
        print("High\n")
    else:
        print("Low\n")
    time.sleep(0.5)
    
 
GPIO.cleanup()

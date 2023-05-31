#-*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

led_pin = 4 #GPIO 4

GPIO.setwarnings(False) #remove warning

GPIO.setmode(GPIO.BCM) #set mode of GPIO as BCM

GPIO.setup(led_pin, GPIO.OUT) #set led in/out

for i in range(10):
    GPIO.output(led_pin, 1) #HIGH(3.3V)
    time.sleep(1)
    GPIO.output(led_pin, 0) #LOW(0V)
    time.sleep(1)
    
GPIO.cleanup()
#-*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

led_pin = 4 #GPIO 4
button_pin = 15 #GPIO 15

GPIO.setwarnings(False) #remove warning

GPIO.setmode(GPIO.BCM) #set mode of GPIO as BCM

GPIO.setup(led_pin, GPIO.OUT) 
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #set switch as pull-down

while 1:
    if GPIO.input(button_pin) == GPIO.HIGH:
        print("High\n")
        GPIO.output(led_pin, 1) #HIGH(3.3V)
    else:
        print("Low\n")
        GPIO.output(led_pin, 0) #LOW(0V)
    time.sleep(0.1)
GPIO.cleanup()


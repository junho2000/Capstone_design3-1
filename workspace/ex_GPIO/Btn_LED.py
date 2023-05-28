#-*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

button_pin = 15 #GPIO 15
led_pin = 4 #GPIO 4

GPIO.setwarnings(False) #remove warning

GPIO.setmode(GPIO.BCM) #set mode of GPIO as BCM

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(led_pin, GPIO.OUT) #set led in/out

light_on = False

def button_callback(channel):
    global light_on
    if light_on == False:
        GPIO.output(led_pin, 1)
        print("LED ON!\n")
        
    else:
        GPIO.output(led_pin, 0)
        print("LED OFF!\n")
    light_on = not light_on

#channel, Rising, callback, bouncetime
GPIO.add_event_detect(button_pin, GPIO.RISING, callback=button_callback, bouncetime=300)

while 1:
    time.sleep(0.1)
GPIO.cleanup()

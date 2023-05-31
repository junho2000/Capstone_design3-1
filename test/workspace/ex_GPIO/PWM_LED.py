#-*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

led_pin = 4 #GPIO 4

GPIO.setwarnings(False) #remove warning
GPIO.setmode(GPIO.BCM) #set mode of GPIO as BCM

GPIO.setup(led_pin, GPIO.OUT) #set led in/out

p = GPIO.PWM(led_pin, 50) #p is instance of PWM, set led_pin to pwm, frequency = 50Hz

p.start(0) #pwm start, dutyratio = 0

try:
    while 1:
        for dc in range(0,101,5):
            p.ChangeDutyCycle(dc) #change dutyratio by setting dc 
            time.sleep(0.1)
        for dc in range(100, -1, -5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
            
except KeyboardInterrupt: #ctrl c -> except
    pass
p.stop() #pwm stop
GPIO.cleanup()
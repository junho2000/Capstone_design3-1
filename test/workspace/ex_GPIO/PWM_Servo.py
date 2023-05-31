#-*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

SERVO_PIN = 18 #GPIO 18

GPIO.setwarnings(False) #remove warning
GPIO.setmode(GPIO.BCM) #set mode of GPIO as BCM

GPIO.setup(SERVO_PIN, GPIO.OUT)

servo = GPIO.PWM(SERVO_PIN, 50)
servo.start(0)

try:
    while True:
        servo.ChangeDutyCycle(7.5) #90'
        time.sleep(1)
        servo.ChangeDutyCycle(12.5) #180'
        time.sleep(1)
        servo.ChangeDutyCycle(2.5) #0'
        time.sleep(1)
except KeyboardInterrupt:
    servo.stop()
    GPIO.cleanup()
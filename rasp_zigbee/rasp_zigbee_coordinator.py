import serial
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

xbee = serial.Serial()
xbee.port = "/dev/ttyAMA1"
xbee.baudrate = 9600
xbee.timeout = 1
xbee.writeTimeout = 1



if xbee.is_open == False:
    xbee.open()
print("Port open status: ", xbee.is_open)
print("Receive & Transfer start")

while True:
    data = xbee.readline().strip()
        
    if data:
        print("Received data: ", data)

xbee.close()
GPIO.cleanup()

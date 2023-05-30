import serial
from datetime import datetime
import RPi.GPIO as GPIO
import pymysql

now = datetime.now()
MarkerID = 0
Latitude = 0
Longitude = 0
NumberPlate = 0
Situation = 0
#zigbee로 데이터를 받으면 sql데이터로 보내는 기능

connection = pymysql.connect(host='mydb.ciskedsbhsct.us-east-2.rds.amazonaws.com', port=3306, user='root', passwd='12341234', db='mydb')
cursor = connection.cursor()
sql = "insert into person('MarkerID','Latitude','Longitude','NumberPlate','Time','Situation') values(%s,%s,%s,%s,%s,%s);"
cursor.execute(sql,(MarkerID, now.date()))
MarkerID += 1
connection.commit()
connection.close()


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


if __name__ == "__main__":

    alter = 0
    while True:
        try:
            while True:
                data = xbee.readline().strip()
                if data:
                    print("Received data: ", data)



        except KeyboardInterrupt:
            break


xbee.close()
GPIO.cleanup()



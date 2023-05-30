import serial
from datetime import datetime
import RPi.GPIO as GPIO
import pymysql

now = datetime.now()
alert_flag = 0
marker_id = 1

#zigbee로 데이터를 받으면 sql데이터로 보내는 기능
#1 -> fire, 2 -> alcohol alert

connection = pymysql.connect(host='mydb.ciskedsbhsct.us-east-2.rds.amazonaws.com', port=3306, user='root', passwd='12341234', db='mydb')
cursor = connection.cursor()

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

    cursor.execute("SELECT * FROM person")
    results = cursor.fetchall()
    
    if alert_flag == 1: #fire
        # Prepare SQL query to INSERT a record into the database
        sql = "INSERT INTO person(MarkerID, Latitude, Longitude, NumberPlate, Time, Situation) VALUES (%s, %s, %s, %s, %s, %s)"
        
        # Prepare the data to be inserted
        marker_id += 1
        latitude = 37.12345  # Replace with the actual latitude value
        longitude = 127.98765  # Replace with the actual longitude value
        number_plate = "1234"  # Replace with the actual number plate
        now = datetime.now()
        now.date()  
        situation = "fire alert"  # Replace with the actual situation description
        
        data = (marker_id, latitude, longitude, number_plate, now, situation)
        
        try:
            # Execute the SQL command
            cursor.execute(sql, data)
            # Commit your changes in the database
            connection.commit()
            print("Fire alert inserted successfully")
            alert_flag = 0
        except:
            # Rollback in case there is any error
            connection.rollback()
            print("Error in inserting Fire alert")
            
    elif alert_flag == 2: #alcohol
        # Prepare SQL query to INSERT a record into the database
        sql = "INSERT INTO person(MarkerID, Latitude, Longitude, NumberPlate, Time, Situation) VALUES (%s, %s, %s, %s, %s, %s)"
        
        # Prepare the data to be inserted
        marker_id += 1
        latitude = 37.12345  # Replace with the actual latitude value
        longitude = 127.98765  # Replace with the actual longitude value
        number_plate = "1234"  # Replace with the actual number plate
        now = datetime.now()
        now.date()  
        situation = "alcohol alert"  # Replace with the actual situation description
        
        data = (marker_id, latitude, longitude, number_plate, now, situation)
        
        try:
            # Execute the SQL command
            cursor.execute(sql, data)
            # Commit your changes in the database
            connection.commit()
            print("Alcohol alert inserted successfully")
            alert_flag = 0
        except:
            # Rollback in case there is any error
            connection.rollback()
            print("Error in inserting Alcohol alert")



xbee.close()
GPIO.cleanup()



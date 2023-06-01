import serial
from datetime import datetime
import RPi.GPIO as GPIO
import pymysql

now = datetime.now()
fire_alert = 0
alcohol_alert = 0
marker_id = 0
latitude = 37.60971110526712  # 미래관 위도 경도
longitude = 126.99762729659923
number_plate = "123가 4568"  #번호판
now = datetime.now()

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

    while True:
        xbee.flushInput()
        data = xbee.readline().strip()
        
        if data == b'fire':
            fire_alert = 1
            
        if data == b'alcohol':
            alcohol_alert = 1
        
        
        if fire_alert == 1: #fire
            
            cursor.execute("SELECT * FROM person")
            results = cursor.fetchall()
            # Prepare SQL query to INSERT a record into the database
            sql = "INSERT INTO person(MarkerID, Latitude, Longitude, NumberPlate, Time, Situation) VALUES (%s, %s, %s, %s, %s, %s)"
            
            # Prepare the data to be inserted
            cursor.execute("SELECT MAX(MarkerID) FROM person")     
            marker = cursor.fetchone()
            max_marker_id = marker[0]
            
            if max_marker_id is None:
                marker_id = 1
            else:
                marker_id = int(max_marker_id) + 1
            
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
                
        if alcohol_alert == 1: #alcohol
            
            cursor.execute("SELECT * FROM person")
            results = cursor.fetchall()
            # Prepare SQL query to INSERT a record into the database
            sql = "INSERT INTO person(MarkerID, Latitude, Longitude, NumberPlate, Time, Situation) VALUES (%s, %s, %s, %s, %s, %s)"
            
            # Prepare the data to be inserted
            cursor.execute("SELECT MAX(CAST(MarkerID AS UNSIGNED)) FROM person")  
            marker = cursor.fetchone()
            max_marker_id = marker[0]
            
            print(max_marker_id)
            
            if max_marker_id is None:
                marker_id = 1
            else:
                marker_id = int(max_marker_id) + 1
            
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
                
        fire_alert = 0
        alcohol_alert = 0


xbee.close()
GPIO.cleanup()
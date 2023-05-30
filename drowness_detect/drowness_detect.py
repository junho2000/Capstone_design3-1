#https://github.com/infoaryan/Driver-Drowsiness-Detection/blob/master/README.md

#Importing OpenCV Library for basic image processing functions
import cv2
# Numpy for array related functions
import numpy as np
# Dlib for deep learning based Modules and face landmark detection
import dlib
#face_utils for basic operations of conversion
from imutils import face_utils
import pymysql
from datetime import datetime
import time

# Connect to the database
connection = pymysql.connect(host='mydb.ciskedsbhsct.us-east-2.rds.amazonaws.com', port=3306, user='root', passwd='12341234', db='mydb')
# Create a cursor object
cursor = connection.cursor()
cursor.execute("SELECT * FROM person")
results = cursor.fetchall()

#Initializing the camera and taking the instance
cap = cv2.VideoCapture(0)
if (not cap.isOpened()):
    print('Error opening video')

#Initializing the face detector and landmark detector
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

#status marking for current state
marker_id = 1
alert_flag = 0
sleep = 0
drowsy = 0
active = 0
status=""
color=(0,0,0)

def compute(ptA,ptB):
	dist = np.linalg.norm(ptA - ptB)
	return dist

def blinked(a,b,c,d,e,f):
	up = compute(b,d) + compute(c,e)
	down = compute(a,f)
	ratio = up/(2.0*down)

	#Checking if it is blinked
	if(ratio>0.24):
		return 2
	elif(ratio>0.2 and ratio<=0.4):
		return 1
	else:
		return 0


while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    h, w, c= frame.shape
    #detected face in faces array
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

        face_frame = frame.copy()
        cv2.rectangle(face_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        landmarks = predictor(gray, face)
        landmarks = face_utils.shape_to_np(landmarks)

        #The numbers are actually the landmarks which will show eye
        left_blink = blinked(landmarks[36],landmarks[37], 
        	landmarks[38], landmarks[41], landmarks[40], landmarks[39])
        right_blink = blinked(landmarks[42],landmarks[43], 
        	landmarks[44], landmarks[47], landmarks[46], landmarks[45])
        
        #Now judge what to do for the eye blinks
        if(left_blink==0 or right_blink==0):
            sleep+=1
            drowsy=0
            active=0
            if(sleep>6):
                status="SLEEPING !!!"
                color = (255,0,0)
                alert_flag = 1
        
        elif(left_blink==1 or right_blink==1):
            sleep=0
            active=0
            drowsy+=1
            if(drowsy>6):
                status="Drowsy !"
                color = (0,0,255)

        else:
            drowsy=0
            sleep=0
            active+=1
            if(active>6):
                status="Active :)"
                color = (0,255,0)
        	
        cv2.putText(face_frame, status, (100,100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color,3)
        if y1 + y1 > h//3*2:
            cv2.putText(face_frame, "Head up!", (300,100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color,3)
        
        for n in range(0, 68):
            (x,y) = landmarks[n]
            cv2.circle(face_frame, (x, y), 1, (255, 255, 255), -1)
    
    cursor.execute("SELECT * FROM person")
    results = cursor.fetchall()
    
    
    
    if alert_flag == 1:
        # Prepare SQL query to INSERT a record into the database
        sql = "INSERT INTO person(MarkerID, Latitude, Longitude, NumberPlate, Time, Situation) VALUES (%s, %s, %s, %s, %s, %s)"
        
        # Prepare the data to be inserted
        marker_id += 1
        latitude = 37.12345  # Replace with the actual latitude value
        longitude = 127.98765  # Replace with the actual longitude value
        number_plate = "1234"  # Replace with the actual number plate
        now = datetime.now()
        now.date()  
        situation = "sleep alert"  # Replace with the actual situation description
        
        data = (marker_id, latitude, longitude, number_plate, now, situation)
        
        try:
            # Execute the SQL command
            cursor.execute(sql, data)
            # Commit your changes in the database
            connection.commit()
            print("Sleep alert inserted successfully")
            alert_flag = 0
        except:
            # Rollback in case there is any error
            connection.rollback()
            print("Error in inserting Sleep alert")

    
            

    cv2.imshow("Frame", frame)
    cv2.imshow("Result of detector", face_frame)
    key = cv2.waitKey(1)
    if key == 27:
      	break
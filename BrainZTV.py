import cv2
import sys
import logging as log
import datetime as dt
from time import sleep
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path

img_counter = 0

cascPath = "haarcascade_frontalface_default.xml" #xml file, keep it in the same dir as brainztv
faceCascade = cv2.CascadeClassifier(cascPath)
log.basicConfig(filename='webcam.log',level=log.INFO) #log file, keep it in the same dir as brainztv

video_capture = cv2.VideoCapture(0)
anterior = 0

while True:
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass

    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
    if anterior != len(faces):
        anterior = len(faces)
        #save picture
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        #log
        log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))
        email = 'senderemail@gmail.com' #enter sender email
        password = 'senderpassword' #enter sender password
        send_to_email = 'receiveremail@gmail.com' #enter receiver email
        subject = 'UPDATE BY BRAINZTV'
        message = 'INTRUDER RILEVATED!'
        file_location = 'opencv_frame_{}.png'.format(img_counter)
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = send_to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        filename = os.path.basename(file_location)
        attachment = open(file_location, "rb")
        part = MIMEBase('application', 'octec-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(part)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        text = msg.as_string()
        server.sendmail(email, send_to_email, text)
        server.quit
        img_counter += 1

    # Display the resulting frame
    cv2.imshow('BrainZTV', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Display the resulting frame
    cv2.imshow('BrainZTV', frame)

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()

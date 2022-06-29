# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 20:08:17 2022

@author: vidhy
"""

import cv2         # Library for openCV
import threading   # Library for threading -- which allows code to run in backend
import playsound   # Library for alarm sound
import smtplib     # Library for email sending
import imghdr
from email.message import EmailMessage
'''
base="http://www.google.com/maps/place/"
address="srit,+rotarypuram,+anantapur,+andhra+pradesh"
add="D.No: xyz,abc colony, def ,Andhra Pradesh"
info=add+'\n'+base+address
'''

info="D.No: xyz,abc colony, def district,Andhra Pradesh"
fire_cascade = cv2.CascadeClassifier('fire_detection_cascade_model.xml') # To access xml file which includes positive and negative images of fire. (Trained images)
                                                                         # File is also provided with the code.

vid = cv2.VideoCapture(0) # To start camera this command is used "0" for laptop inbuilt camera and "1" for USB attahed camera
runOnce = False # created boolean


def play_alarm_sound_function():# defined function to play alarm post fire detection using threading

    playsound.playsound('fire_alarm.mp3',True) # to play alarm # mp3 audio file is also provided with the code.
    print("Fire alarm end") # to print in console
       

def send_mail_function(): # defined function to send mail post fire detection using threading
    try:
        Sender_Email = "pavithrachittari@gmail.com"
        Reciever_Email ='pavithrachittari@gmail.com'
        Password = 'vidhyadhari'
        
        newMessage = EmailMessage()                         
        newMessage['Subject'] = "ALERT!! Fire accident reported" 
        newMessage['From'] = Sender_Email                   
        newMessage['To'] =  Reciever_Email          
        newMessage.set_content(info) 

        with open('NewPicture.jpg', 'rb') as f:
            image_data = f.read()
            image_type = imghdr.what(f.name)
            image_name = f.name
        newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            
            smtp.login(Sender_Email, Password)              
            smtp.send_message(newMessage)
            print('mail sent')
        
    except Exception as e:
        print(e) # To print error if any


		
while(True):
    Alarm_Status = False
    ret, frame = vid.read() # Value in ret is True # To read video frame
    ret, frame1 = vid.read()
    difference = cv2.absdiff(frame, frame1)
    gray1 = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray1, (5,5), 0)
    _, threshold = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilate = cv2.dilate(threshold, None, iterations=3)
    contour, _ = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, contour, -1, (0, 0, 255), 2)
    cv2.imshow("image", frame)
    frame = frame1
    ret, frame1 = vid.read()
    if cv2.waitKey(40) == ord('q'):
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # To convert frame into gray color
    fire = fire_cascade.detectMultiScale(frame, 1.2, 5) # to provide frame resolution
    
    ## to highlight fire with square 
    
    for (x,y,w,h) in fire:
        cv2.rectangle(frame,(x-20,y-20),(x+w+20,y+h+20),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        
        
        print("Fire alarm initiated")
        threading.Thread(target=play_alarm_sound_function).start()  # To call alarm thread
        
        result = True
        while(result):
            ret,frame = vid.read()
            cv2.imwrite("NewPicture.jpg",frame)
            result = False
        if runOnce == False:
            print("Mail send initiated")
            threading.Thread(target=send_mail_function).start() # To call alarm thread
            runOnce = True
        if runOnce==True:
            print("Mail is already sent once")
            runOnce=True
            
        

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
vid.release()
cv2.destroyAllWindows()
__author__ = 'Winston'
import cv2
import time

import serial

ser = serial.Serial('COM3', 9600)

cap=cv2.VideoCapture(1)
time.sleep(5)
ret,img = cap.read()
time.sleep(5)
ret,img = cap.read()
time.sleep(5)
ret,pic = cap.read()
referenceFrame = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
referenceFrame = cv2.GaussianBlur(referenceFrame, (21,21),0)
counter = 1
height,width = referenceFrame.shape[:2]

while (True):
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    ret, frame = cap.read()
    #ret is a boolean, img is the image

    cv2.imshow("camera",frame)
    #leave the loop if the image cant be returned

    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("greyscaled",grey)

    blur = cv2.GaussianBlur(grey, (21,21),0)
    cv2.imshow("blur",blur)
    #greyscale and gaussian blurs each frame
    counter+=1


    delta =cv2.absdiff(referenceFrame,blur)
   # cv2.imshow("reference",referenceFrame)

    cv2.imshow("diff",delta)

    threshold = cv2.threshold(delta,25,255,cv2.THRESH_BINARY)[1]
    #if less than 25 set black, greater 255 set max
    #threshold = cv2.dilate(threshold, None, iterations=2)
    cv2.imshow("thresh",threshold)
    thresh = cv2.dilate(threshold, None, iterations=30)
    cv2.imshow("dilated",thresh)
    _, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                                    #source, retrieval mode, approximation method
    for cnt in contours:

        if cv2.contourArea(cnt) < 10000:
            ser.write(chr(0))
            continue

        x,y,w,h = cv2.boundingRect(cnt)
        print "x is {} y is {} w is {} h is {}, center will be at {},{}".format(x,y,w,h,x+(w/2),y+(h/2))

        xcoordinate = float(x+(w/2))
        frac =(xcoordinate)/float(width)
        angle = int(66*frac)
        #calculate angle
        print frac
        print angle
        #print angle and related
        ser.write(chr(angle+57))
        ser.write(chr(1))
        print "fire"
        #send over serial
        cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)



    cv2.imshow("rectanglepls",frame)
cap.release()
cv2.destroyAllWindows()

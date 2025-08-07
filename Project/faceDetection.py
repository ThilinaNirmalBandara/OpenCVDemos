import cv2
import numpy as np

faceCascade = cv2.CascadeClassifier("Project/haarcascade_frontalface_default.xml")

# https://github.com/opencv/opencv/tree/master/data/haarcascades

cap = cv2.VideoCapture(0)

while(1):
    _,img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.3 , 5)

    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)

    cv2.imshow("Face Detector",img)
    k = cv2.waitKey(30) & 0xFF
    if(k == 27):
        break

cap.release()
cv2.destroyAllWindows()



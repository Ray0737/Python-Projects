import cv2 as cv
import numpy as np
import datetime as dt


# img = np.full((600,600,3),255,dtype =np.uint8)
# font = cv.FONT_HERSHEY_TRIPLEX

# cv.rectangle(img,(200,250),(400,350),(255,205,148),-1)
# cv.circle(img,(300,300),50,(49,59,235),-1)
# cv.line(img,(0,0),(600,600),(166,235,157),5)
# cv.putText(img,'OpenCV Homework',(150,570), font, 1,(199,123,154),2,cv.LINE_AA)
# cv.imshow('test',img)
# cv.waitKey(0)
# cv.destroyAllWindows()

dtdatetime=str(dt.datetime.now())
font = cv.FONT_HERSHEY_TRIPLEX
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame.")
        break

    cv.circle(frame,(320,240),50,(161,255,130),3)
    cv.rectangle(frame,(0,0),(640,480),(245,160,118),20)
    cv.line(frame,(0,0),(640,480),(188,188,245),5)
    cv.putText(frame," Live video : ",(10,50), font, 0.8,(199,123,154),2,cv.LINE_AA)
    cv.putText(frame,dtdatetime,(190,50), font, 0.8,(255,255,255),2,cv.LINE_AA)
    cv.imshow('Webcam', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv.destroyAllWindows()
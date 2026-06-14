import cv2 as cv
import numpy as np
import datetime as dt

img = np.zeros((600,600,3),dtype =np.uint8)
font = cv.FONT_HERSHEY_SCRIPT_SIMPLEX
dtdatetime=str(dt.datetime.now())
cv.line(img,(0,300),(600,500),(255,194,198),1)
cv.arrowedLine(img,(60,0),(123,570),(150,163,255),4)
cv.rectangle(img,(505,50),(250,250),(255,255,120),10)
cv.circle(img,(420,435),85,(255,161,89),20)
cv.putText(img,'View 023546',(380,570), font, 1,(255,255,255),2,cv.LINE_AA)
cv.putText(img,dtdatetime,(80,10), font, 1,(255,255,255),2,cv.LINE_AA)
cv.imshow('test',img)
cv.waitKey(0)
cv.destroyAllWindows()
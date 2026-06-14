import cv2 as cv
import numpy as np

img1 = np.full((500,500,3),255,dtype =np.uint8)
img2 = np.full((500,500,3),255,dtype =np.uint8)
img3 = cv.imread('R.jpg')

upper_green = np.array([100,255,130])
lower_green = np.array([0,50,0])
mask = cv.inRange(img3,lower_green,upper_green)
result = cv.bitwise_and(img3,img3,mask=mask)


cv.rectangle(img1,(70,70),(430,430),(245,160,118),-1)
cv.circle(img2,(250,250),200,(245,160,118),-1)

bitwise_and = cv.bitwise_and(img1,img2)
bitwise_or = cv.bitwise_or(img1,img2)
bitwise_not = cv.bitwise_not(img1,img2)
bitwise_xor = cv.bitwise_xor(img1,img2)

# cv.imshow('Rectangle',img1)
# cv.imshow('circle',img2)
# cv.imshow('AND',bitwise_and)
# cv.imshow('OR',bitwise_or)
# cv.imshow('NOT',bitwise_not)
# cv.imshow('XOR',bitwise_xor)
# cv.imshow('origin',img3)
# cv.imshow('detect color mask',mask)
# cv.imshow('result ', result)
cv.waitKey(0)
cv.destroyAllWindows()
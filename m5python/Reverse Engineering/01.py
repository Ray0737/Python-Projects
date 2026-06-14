import cv2 as cv

# Read and show image
# cv.imread ('img path',(0,1,-1)) | 0 = black, 1 = white, -1 = origin
img = cv.imread('m5python/Reverse Engineering/test/test.png') 

cv.imshow("test", img) # show image
cv.waitKey(0) # wait for key press
cv.destroyAllWindows() # close all windows
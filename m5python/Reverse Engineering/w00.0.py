import cv2 as cv
import numpy as np
import random
import matplotlib.pyplot as plt

img = cv.imread('m5python/Reverse Engineering/test/test.png',1) # cv.imshow ('img name',(0,1,-1)) | 0 = black, 1 = white, -1 = origin
print(img)
print(img.shape) # (height, width, 3 Color Layers )
cv.imshow('Test Image', img) # Show the binary image in a window
cv.waitKey(0) # Press 0 to close the window
cv.destroyAllWindows() # Related function after press 0
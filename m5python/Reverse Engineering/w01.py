import cv2 as cv
import numpy as np

# How to do: Read image then go thorugh all pixel and check their RBG value 
# to convert to gray then sort binary by using the threshold as the divider between black and white

# 1.
img = cv.imread('m5python/Reverse Engineering/test/test.png') # [cite: 74, 75]
height, width, channels = img.shape

# 2.(Binary Image)
binary_img = np.zeros((height, width), dtype=np.uint8)

#RGB Threshold 128/256 1/2  
threshold_value = 128

for y in range(height):
    for x in range(width):

        b = img[y, x, 0]
        g = img[y, x, 1]
        r = img[y, x, 2]
        
        gray = 0.114 * b + 0.587 * g + 0.299 * r
        
        if gray >= threshold_value:
            binary_img[y, x] = 255  
        else:
            binary_img[y, x] = 0    

cv.imshow('Binary Image Output', binary_img) # Show the binary image in a window
cv.waitKey(0) # Press 0 to close the window
cv.destroyAllWindows() # Related function after press 0


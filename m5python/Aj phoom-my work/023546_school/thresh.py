import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np

thresh_value = [75,100,128,180,230]

img = cv.imread('baht.jpg')
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
plt.subplot(231, title="gray" % (thresh_value), xticks=[],yticks=[]) 
plt.imshow(gray, cmap="gray")
for i in range(len(thresh_value)):
    thresh, result = cv.threshold (gray, thresh_value[i], 255, cv.THRESH_BINARY_INV) 
    plt.subplot(232+i, title="Threshold %d" % (thresh_value[i]), xticks=[],yticks=[]) 
    plt.imshow(result, cmap="gray")
plt.show()
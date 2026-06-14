import cv2 as cv

import numpy as np
img = cv.imread('R.jpg')
print(img)

h,w,_ = img.shape


# down_w =w//2
# down_h = h//2
# down_p = (down_w,down_h)

# rezied_down = cv.resize(img,down_p, interpolation= cv.INTER_LINEAR)

# up_p = (w*2,h*2)
# rezied_up = cv.resize(img,up_p, interpolation= cv.INTER_LINEAR)

# crop = img[200:820,1000:1800]

# cv.imshow('ttr',rezied_down)
# cv.waitKey(0)
# cv.imshow('ttr',crop)
# cv.waitKey(0) 
# cv.destroyAllWindows()
# a= np.array([[0.5,0,100],
#              [0,0.5,100]])

# new = (cv.warpAffine(img,a,(w,h))[:,:,::-1])
# cv.imshow('R.jpg',new)
cv.waitKey(0)
cv.destroyAllWindows()


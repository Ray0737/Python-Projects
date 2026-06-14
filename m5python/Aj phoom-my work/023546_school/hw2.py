import cv2 as cv
import numpy as np

img = cv.imread('m5python/Aj phoom-my work/023546_school/R.jpg')
h,w,_ = img.shape

a= np.array([[0.5,0,-90],
             [0,0.5,100]])
new = (cv.warpAffine(img,a,(w,h))[:,:,::1])
cv.imshow('R.jpg',new)
cv.waitKey(0)
cv.destroyAllWindows()

# rorate_metrix = cv.getRotationMatrix2D(center=(990, 540), angle =27, scale= 0.5)
# rorated_imge = cv.warpAffine(img, rorate_metrix, dsize=(w,h))
# cv.imshow('R.jpg',rorated_imge)
# cv.waitKey(0)
# cv.destroyAllWindows()

# up_weight= (w,h//2)
# rezied_Up = cv.resize(img,up_weight, interpolation= cv.INTER_LINEAR)
# cv.imshow('weightttttttt',rezied_Up)
# cv.waitKey(0)

# a= np.array([[0.5,0,100],
#              [0,0.5,0]])
# new = (cv.warpAffine(img,a,(w,h))[:,:,::1])
# rorate_metrix = cv.getRotationMatrix2D(center=(990, 540), angle =92, scale= 0.5)
# rorated_imge = cv.warpAffine(new, rorate_metrix, dsize=(w,h))
# up_weight= (w//2,h)
# rezied_Up = cv.resize(rorated_imge,up_weight, interpolation= cv.INTER_LINEAR)
# cv.imshow('final',rezied_Up)
# cv.waitKey(0)



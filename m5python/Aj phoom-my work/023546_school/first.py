import cv2 as cv
import numpy as np

img = cv.imread('m5python/Aj phoom-my work/023546_school/img.jpg')

gray = np.zeros((img.shape[0],img.shape[1]), dtype =np.uint8)

for i in range(img.shape[0]):
    for x in range(img.shape[1]):
        gray[i,x] = int(0.114*img[i,x,0]+ 0.587*img[i,x,1]+ 0.299*img[i,x,2])
        gray[i,x] = np.clip(gray[i,x], 0, 255)

gray = np.where(gray < 127, 0, 225).astype(np.uint8)


print(gray)
cv.imshow('gray imge',gray)
cv.waitKey(0)
cv.destroyAllWindows()
cv.imwrite('gray image.jpg',gray)

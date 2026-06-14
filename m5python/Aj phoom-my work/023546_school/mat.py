import matplotlib.pyplot as plt
import cv2 as cv

# x =[20,71,96,118]
# y =[10,52,76,89]
# plt.plot(x,y)
# plt.show()
img = cv.imread('R.jpg')
img = cv.cvtColor(img,cv.COLOR_BGR2RGB)
plt.imshow(img[:,:,::-1])
plt.show()

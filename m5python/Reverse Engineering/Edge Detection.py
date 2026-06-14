import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

#--------------------------------------------------Sobel--------------------------------------------------#

# Load image in grayscale (0)
img = cv.imread("m5python/Aj phoom-my work/023546_school/baht.jpg", 0)

# sobel = cv2.Sobel(1, 2, 3, 4)
# 1 คือ รูปภาพ (Image)
# 2 คือ ชนิดตัวแปรใน Array (กำหนดค่าเป็น -1 เพื่อให้อ้างอิงกับ Array ของภาพต้นฉบับ) (Depth)
# 3 คือ ตัวกรองในแนวแกน X (dx)
# 4 คือ ตัวกรองในแนวแกน Y (dy)

sobelX = cv.Sobel(img, -1, 1, 0)
sobelY = cv.Sobel(img, -1, 0, 1)
sobelXY = cv.bitwise_or(sobelX, sobelY)

images = [img, sobelX, sobelY, sobelXY]
titles = ["Original", "SobelX", "SobelY", "SobelXY"]

for i in range(len(images)):
    plt.subplot(2, 2, i+1)
    plt.imshow(images[i], cmap="gray")
    plt.title(titles[i])
    plt.xticks([]), plt.yticks([])

plt.show()

#--------------------------------------------------Laplacian--------------------------------------------------#

img = cv.imread("m5python/Aj phoom-my work/023546_school/baht.jpg")
# lap = cv.Laplacian(1,2)
# # 1 คือ รูปภาพ
# # 2 คือ ชนิดตัวแปรใน Array(กำหนดค่าเป็น -1 เพื่อให้อ้างอิงกับ Array ของภาพต้นฉบับ)

lap = cv.Laplacian(img,-1)

cv.imshow("Original",img)
cv.imshow("Laplacian",lap)

cv.waitKey(0)
cv.destroyAllWindows()

#--------------------------------------------------Canny--------------------------------------------------#

# Load the image in grayscale (the 0 flag indicates grayscale)
img = cv.imread("m5python/Aj phoom-my work/023546_school/baht.jpg",0)

# # canny = cv2.Canny(1,2,3)
# # 1 คือ รูปภาพ (Image)
# # 2 คือ เทรชโฮลด์ค่าที่ 1 (Threshold 1)
# # 3 คือ เทรชโฮลด์ค่าที่ 2 (Threshold 2)

# Apply Canny Edge Detection
canny = cv.Canny(img, 50, 200)

# Display the original and processed images
cv.imshow("Original", img)
cv.imshow("Canny", canny)

# Wait for a key press and then close all windows
cv.waitKey(0)
cv.destroyAllWindows()

#--------------------------------------------------Hough--------------------------------------------------#

# Read the image
img = cv.imread("m5python/Reverse Engineering/69871_0.jpg")

# Convert to grayscale
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# Apply Canny edge detection
edges = cv.Canny(gray, 50, 150, apertureSize=3)

# Use Probabilistic Hough Line Transform to detect lines
lines = cv.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)

# Iterate through the detected lines and draw them on the original image
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Display the result
cv.imshow("HoughLines", img)

cv.waitKey(0)
cv.destroyAllWindows()
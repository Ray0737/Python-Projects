import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

lower_green = np.array([35, 60, 40])   # Light green
upper_green = np.array([85, 255, 255])

lower_gray = np.array([0, 0, 50])      # Very low saturation, medium brightness
upper_gray = np.array([180, 30, 200])

lower_white = np.array([0, 0, 200])
upper_white = np.array([180, 30, 255])

List_colors = [(lower_green,upper_green),
               (lower_gray,upper_gray),
               (lower_white,upper_white)]
str_color = ['green','gray','white']

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame.")
        break
    roi = frame[10:450,180:400]
    hsv = cv.cvtColor(roi,cv.COLOR_BGR2HSV)
    mask_green = cv.inRange(hsv, lower_green, upper_green)
    mask_gray = cv.inRange(hsv, lower_gray, upper_gray)
    mask_white = cv.inRange(hsv, lower_white, upper_white)

    result_green = cv.bitwise_and(frame, frame, mask=mask_green)
    result_gray = cv.bitwise_and(frame, frame, mask=mask_gray)
    result_white = cv.bitwise_and(frame, frame, mask=mask_white)
    cv.imshow('Original', frame)
    cv.imshow('Green LEGO', result_green)
    cv.imshow('Gray LEGO', result_gray)
    cv.imshow('White LEGO', result_white)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv.destroyAllWindows()
import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

lower_green = np.array([30, 146, 58])
upper_green = np.array([47, 255, 149])

lower_gray = np.array([60, 47, 10])
upper_gray = np.array([122, 255, 82])

lower_white = np.array([95, 0, 149])
upper_white = np.array([160, 64, 206])

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    mask_green = cv.inRange(hsv, lower_green, upper_green)
    mask_gray = cv.inRange(hsv, lower_gray, upper_gray)
    mask_white = cv.inRange(hsv, lower_white, upper_white)

    combined_mask = cv.bitwise_or(mask_green, mask_gray)
    combined_mask = cv.bitwise_or(combined_mask, mask_white)

    result_combined = cv.bitwise_and(frame, frame, mask=combined_mask)

    # Optional: Display individual masks
    # result_green = cv.bitwise_and(frame, frame, mask=mask_green)
    # result_gray = cv.bitwise_and(frame, frame, mask=mask_gray)
    # result_white = cv.bitwise_and(frame, frame, mask=mask_white)

    # Show the results
    cv.imshow('Original', frame)
    cv.imshow('Detected Colors (Green, Gray, White)', result_combined)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

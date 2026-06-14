import cv2 as cv
import numpy as np
 
cap = cv.VideoCapture('Sequence 01.mp4')
# scale = 90

ret, frame = cap.read()
if not ret:
    print("Can't open this video")
    cap.release()
    exit()

h, w = frame.shape[:2]
path_map = np.zeros((h, w, 3), dtype=np.uint8)
 
points = []
 
while True:
    ret, frame = cap.read()
    if not ret:
        break
 
    # frame_small= cv.resize(frame, (int(w * scale / 100), int(h * scale / 100)))
    # path_map_small = cv.resize(path_map, (int(w * scale / 100), int(h * scale / 100)))

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    lower_blue = np.array([100, 150, 100])
    upper_blue = np.array([120, 255, 255])
 
    mask = cv.inRange(hsv, lower_blue, upper_blue)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)

    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv.contourArea)
        area = cv.contourArea(largest_contour)
        if area > 300: 
            M = cv.moments(largest_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                center = (cx, cy)
                points.append(center)
                cv.circle(frame, center, 5, (96, 83, 254), -1)
                x, y, w, h = cv.boundingRect(largest_contour)
                cv.rectangle(frame, (x, y), (x + w, y + h), (253, 208, 112), 2)

    for i in range(1, len(points)):
        cv.line(frame, points[i - 1], points[i], (96, 83, 254), 2)
        cv.line(path_map, points[i - 1], points[i], (255, 255, 255), 2)

    cv.imshow('Frame', frame)
    cv.imshow('Path Map', path_map)
 
    key = cv.waitKey(30) & 0xFF
    if key == ord('s'):
        cv.imwrite('frame_with_path.png', frame)
        cv.imwrite('path_map.png', path_map)
        print("บันทึกภาพเรียบร้อยแล้ว")
    elif key == ord('q'):
        break
 
cap.release()
cv.destroyAllWindows()
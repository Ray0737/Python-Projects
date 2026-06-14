import cv2
import numpy as np
from lane_sim import LaneSim
 
def detect_lane_center(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   
    height, width = gray.shape
    horizon_y = int(height * 0.45)
 
    roi = gray[horizon_y:, :]
 
    edges = cv2.Canny(roi, 50, 150)
   
    center_points = []
    left_edge_points = []
    right_edge_points = []
 
    for y in range(edges.shape[0]):
        row = edges[y]
        left_indices = np.where(row > 0)[0]
        if len(left_indices) >= 2:
            left = left_indices[0]
            right = left_indices[-1]
            center = (left + right) // 2
            center_points.append((center, y + horizon_y))
            left_edge_points.append((left, y + horizon_y))
            right_edge_points.append((right, y + horizon_y))
        else:
            continue
 
    center_img = img.copy()
    for i in range(len(center_points) - 1):
        cv2.line(center_img, center_points[i], center_points[i+1], (130, 58, 255), 2)
    for i in range(len(left_edge_points) - 1):
        cv2.line(center_img, left_edge_points[i], left_edge_points[i+1], (255, 5, 163), 3)
    for i in range(len(right_edge_points) - 1):
        cv2.line(center_img, right_edge_points[i], right_edge_points[i+1], (255, 5, 163), 3)
 
    return center_img
 
 
sim = LaneSim(width=1920, height=1080)
while True:
    key = cv2.waitKey(1) & 0xFF
    action = -1 if key in (ord('a'),81) else 1 if key in (ord('d'),83) else 0
    if key == 27: break
    frame = sim.step(action)
    frame_with_center = detect_lane_center(frame)
    cv2.imshow('LaneSim', frame_with_center)
cv2.destroyAllWindows()
 
import cv2 as cv
import numpy as np
import random
import matplotlib.pyplot as plt

"""
OPENCV PYTHON TUTORIAL: FROM BASICS TO APPLICATIONS
--------------------------------------------------
This file covers:
1. Media Loading   2. Transformations   3. Drawing
4. Mouse Events    5. Bitwise & Logic   6. Thresholding
7. Morphological   8. Contour Projects
"""

# =================================================================
# 1. IMAGE & VIDEO BASICS
# =================================================================
# Load and show a static image
img_path = "m5python/Aj phoom-my work/023546_school/R.jpg"
img = cv.imread(img_path)
if img is not None:
    cv.imshow('1.1 Static Image', img)
    cv.waitKey(0)

# Video Playback Logic
capture = cv.VideoCapture('m5python/Aj phoom-my work/work/Sequence 01.mp4')
while capture.isOpened():
    isTrue, frame = capture.read()
    if not isTrue: break
    cv.imshow('1.2 Video Playback', frame)
    if cv.waitKey(20) & 0xFF == ord('q'): # Press 'q' to exit
        break
capture.release()
cv.destroyAllWindows()


# =================================================================
# 2. RESIZING & TRANSFORMATIONS
# =================================================================
def rescaleFrame(frame, scale=0.75):
    """Rescales an image or video frame by a percentage."""
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    return cv.resize(frame, (width, height), interpolation=cv.INTER_AREA)

img = cv.imread(img_path)
if img is not None:
    # Resizing
    frame_resized = rescaleFrame(img, scale=0.5)
    cv.imshow('2.1 Resized', frame_resized)

    # Cropping [y_start:y_end, x_start:x_end]
    cropped_image = img[80:280, 150:330]
    cv.imshow("2.2 Cropped", cropped_image)

    # Rotation
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    matrix = cv.getRotationMatrix2D(center, 45, 1.0) # 45 degrees, no zoom
    rotated_image = cv.warpAffine(img, matrix, (w, h))
    cv.imshow("2.3 Rotated", rotated_image)
    cv.waitKey(0)
    cv.destroyAllWindows()


# =================================================================
# 3. DRAWING & SHAPES
# =================================================================
# Create a black square canvas (500x500 pixels, 3 channels)
blank = np.zeros((500, 500, 3), dtype='uint8')

# Draw shapes (Parameters: img, start_point, end_point, color_BGR, thickness)
cv.rectangle(blank, (0,0), (250, 500), (0,0,255), thickness=cv.FILLED) 
cv.circle(blank, (blank.shape[1]//2, blank.shape[0]//2), 40, (0,0,255), thickness=3)
cv.line(blank, (0,0), (250, 250), (0,255,0), thickness=3)
cv.putText(blank, "Hello OpenCV", (50, 255), cv.FONT_HERSHEY_TRIPLEX, 1.0, (255,255,255), 2)

cv.imshow('3. Drawing Shapes', blank)
cv.waitKey(0)


# =================================================================
# 4. INTERACTIVE MOUSE EVENTS (Color Picker & Drawing)
# =================================================================
# This section demonstrates how to handle mouse clicks
img_event = cv.imread(img_path)
points = []

def mouse_callback_demo(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        # Get BGR values at click
        blue, green, red = img_event[y, x]
        color_text = f"BGR: {blue},{green},{red}"
        
        # Draw interaction
        cv.circle(img_event, (x, y), 10, (0, 255, 0), -1)
        points.append((x, y))
        if len(points) > 1:
            cv.line(img_event, points[-1], points[-2], (255, 255, 255), 2)
            
        cv.putText(img_event, color_text, (x, y - 15), 1, 1.0, (255, 255, 255), 2)
        cv.imshow('4. Mouse Interactions', img_event)

if img_event is not None:
    cv.imshow('4. Mouse Interactions', img_event)
    cv.setMouseCallback('4. Mouse Interactions', mouse_callback_demo)
    cv.waitKey(0)
    cv.destroyAllWindows()


# =================================================================
# 5. BITWISE OPERATIONS & COLOR FILTERING
# =================================================================
# Bitwise operations are used for masking and image logic
rect_img = np.zeros((400, 400), dtype='uint8')
circ_img = np.zeros((400, 400), dtype='uint8')

cv.rectangle(rect_img, (50, 50), (350, 350), 255, -1)
cv.circle(circ_img, (200, 200), 200, 255, -1)

# Logic Operations
bit_and = cv.bitwise_and(rect_img, circ_img) # Intersection
bit_or  = cv.bitwise_or(rect_img, circ_img)  # Union
bit_xor = cv.bitwise_xor(rect_img, circ_img) # Non-overlapping

# Show logic
titles = ['Rectangle', 'Circle', 'AND', 'OR', 'XOR']
images = [rect_img, circ_img, bit_and, bit_or, bit_xor]
for i in range(5):
    plt.subplot(1, 5, i+1), plt.imshow(images[i], 'gray'), plt.title(titles[i])
    plt.xticks([]), plt.yticks([])
plt.show()


# =================================================================
# 6. THRESHOLDING & ADAPTIVE METHODS
# =================================================================
# Thresholding turns grayscale images into binary (Black & White)
img_gray = cv.imread(img_path, 0) # Load as grayscale

# Simple Threshold: Everything above 127 becomes White (255)
_, thresh_simple = cv.threshold(img_gray, 127, 255, cv.THRESH_BINARY)

# Adaptive Threshold: Calculates threshold for small regions (handles shadows)
thresh_adapt = cv.adaptiveThreshold(img_gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv.THRESH_BINARY, 11, 2)

plt.figure(figsize=(10,5))
plt.subplot(1,2,1), plt.imshow(thresh_simple, 'gray'), plt.title('Simple Threshold')
plt.subplot(1,2,2), plt.imshow(thresh_adapt, 'gray'), plt.title('Adaptive Gaussian')
plt.show()


# =================================================================
# 7. MORPHOLOGICAL OPERATIONS
# =================================================================
# Used to clean up noise in binary images
kernel = np.ones((5, 5), np.uint8)
erosion = cv.erode(thresh_simple, kernel, iterations=1)
dilation = cv.dilate(thresh_simple, kernel, iterations=1)
opening = cv.morphologyEx(thresh_simple, cv.MORPH_OPEN, kernel) # Remove white noise

# =================================================================
# 8. FINAL PROJECT: CONTOUR COIN COUNTER
# =================================================================
# This part integrates filtering, morphology, and contours.

coin_values = {
    '1': {'min': 27, 'max': 28, 'value': 1},
    '2': {'min': 29, 'max': 33, 'value': 2},
    '10': {'min': 34, 'max': 40, 'value': 10}
}

def classify_coin(radius):
    for label, info in coin_values.items():
        if info['min'] <= radius <= info['max']:
            return label
    return None

# Load coin video
cap = cv.VideoCapture('m5python/Aj phoom-my work/023546_school/coinn.mp4')
kernel_ellipse = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    # Pre-processing
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (11, 11), 0)
    _, thresh = cv.threshold(blur, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
    
    # Cleaning the image
    opened = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel_ellipse, iterations=1)
    closed = cv.morphologyEx(opened, cv.MORPH_CLOSE, kernel_ellipse, iterations=2)

    # Finding Contours
    contours, _ = cv.findContours(closed, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    count = 0
    total = 0
    for cnt in contours:
        area = cv.contourArea(cnt)
        if 1000 < area < 40000:
            (x, y), radius = cv.minEnclosingCircle(cnt)
            coin_type = classify_coin(int(radius))
            
            if coin_type:
                count += 1
                total += coin_values[coin_type]['value']
                cv.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
                cv.putText(frame, f"{coin_type}B", (int(x)-10, int(y)), 1, 1, (255,255,255), 2)

    cv.putText(frame, f"Total Baht: {total}", (50, 100), 1, 2, (0, 255, 255), 3)
    cv.imshow("8. Final Project: Coin Counter", frame)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
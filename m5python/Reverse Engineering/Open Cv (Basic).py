import cv2 as cv
import numpy as np
import random
import matplotlib.pyplot as plt

#--------------------------------------------------Image Read--------------------------------------------------#
img = cv.imread('m5python/Reverse Engineering/test/test.png',1) # cv.imshow ('img name',(0,1,-1)) | 0 = black, 1 = white, -1 = origin
print(img) #print out RBG
print(img.shape) # (height, width, 3 Color Layers )
cv.imshow('Test Image', img) # Show the binary image in a window
cv.waitKey(0) # Press 0 to close the window
cv.destroyAllWindows() # Related function after press 0
cv.imwrite("Cropped Image.jpg", img) # Saves the new image (Able to convert file type using Py)

#--------------------------------------------------Image Show--------------------------------------------------#
img = cv.imread("m5python/Aj phoom-my work/023546_school/R.jpg")
cv.imshow('Test', img)
cv.waitKey(0)

#Video Show
capture = cv.VideoCapture('m5python/Aj phoom-my work/work/Sequence 01.mp4')
while True:
    isTrue, frame = capture.read()
    cv.imshow('Video',frame)
    if cv.waitKey(20) & 0xFF ==ord('d'): # if press d
        break
    
capture.release()
cv.destroyAllWindows()

#--------------------------------------------------Resize--------------------------------------------------#
img = cv.imread("m5python/Aj phoom-my work/023546_school/R.jpg")

def rescaleFrame(frame,scale=0.75):
    width = int(frame.shape[1]*scale)
    height = int(frame.shape[0]*scale)
    dimensions = (width,height)
    return cv.resize(frame,dimensions,interpolation=cv.INTER_AREA)

def changeRes(width,height):
    capture.set(3,width)
    capture.set(4,height)
    
frame_resized = rescaleFrame(img)
cv.imshow('Resized',frame_resized)
cv.waitKey(0)

#--------------------------------------------------Blank Page--------------------------------------------------#

blank = np.zeros((500,500,3),dtype='uint8') #blank page
cv.imshow('Blank',blank)

img = cv.imread("m5python/Aj phoom-my work/023546_school/R.jpg")
cv.imshow('Test', img)

blank[200:300,300:400] = 0,0,255 # red
cv.imshow('Red',blank)

cv.rectangle(blank,(0,0),(250,500),(0,0,255),thickness=cv.FILLED) #250,500 = width x height
cv.imshow('Rectangle',blank)
cv.rectangle(blank,(0,0),(blank.shape[1]//2,blank.shape[0]//2),(0,0,255),thickness=cv.FILLED) #square
cv.imshow('Rectangle',blank)
cv.circle(blank,(blank.shape[1]//2,blank.shape[0]//2),40,(0,0,255),thickness=3)
cv.imshow('Circle',blank)
cv.line(blank,(0,0),(blank.shape[1]//2,blank.shape[0]//2),(0,0,255),thickness=3)
cv.imshow('line',blank)
cv.putText(blank,"Hello",(0,255),cv.FONT_HERSHEY_TRIPLEX,1.0,(0,255,0),2)
cv.imshow('Text',blank)
cv.waitKey(0)

#--------------------------------------------------Crop--------------------------------------------------#

img = cv.imread('m5python/Aj phoom-my work/023546_school/R.jpg')
# Select rows 80 to 280 and columns 150 to 330
cropped_image = img[80:280, 150:330] 

cv.imshow("cropped", cropped_image)
cv.imwrite("Cropped Image.jpg", cropped_image) # Saves the new image
cv.waitKey(0)

#--------------------------------------------------Rotation--------------------------------------------------#

# Load the image
img = cv.imread('m5python/Aj phoom-my work/023546_school/R.jpg')
(h, w) = img.shape[:2] # Get image height and width

# 1. Define the rotation parameters
center = (w // 2, h // 2)  # Rotate around the center of the image
angle = 45                 # Degrees to rotate (positive for counter-clockwise)
scale = 1.0                # Keep the same scale (no zoom)

# 2. Get the rotation matrix (OpenCV helper function)
# This creates the 2x3 matrix mentioned in the document
matrix = cv.getRotationMatrix2D(center, angle, scale)

# 3. Apply the rotation using warpAffine
# This moves every pixel to its new rotated position
rotated_image = cv.warpAffine(img, matrix, (w, h))

# Display the results
cv.imshow("Original", img)
cv.imshow("Rotated Image", rotated_image)
cv.waitKey(0)
cv.destroyAllWindows()

#--------------------------------------------------Mouse Click Event (0)--------------------------------------------------#

#Show text, Show RGB of cord, Show Coord when pressed

img = cv.imread('R.jpg')

def click_position(event, x, y, flags, param):
    # Check specifically for a left mouse button click
    if event == cv.EVENT_LBUTTONDOWN:
        # Extract individual BGR color values from the pixel at the clicked (y, x) position
        # OpenCV uses (row, col) indexing, which maps to (y, x)
        blue = img[y, x, 0]  # Channel 0 is Blue
        green = img[y, x, 1] # Channel 1 is Green
        red = img[y, x, 2]   # Channel 2 is Red
        
        # Format strings for the color values and the coordinate positions
        text = ("R:G:B=%s,%s,%s" % (red, green, blue))
        cord = ("x = %s,y=%s" % (x, y))

        display_text = f'totoro {cord} : {text}'
        
        # Draw the combined text onto the image
        # Parameters: (image, text, position, font, scale, BGR_color, thickness)
        cv.putText(img, display_text, (x, y), 1, 3, (255, 223, 194), 3)

        cv.imshow('click puttext', img)


cv.imshow('click puttext', img)
cv.setMouseCallback('click puttext', click_position)
cv.waitKey(0)
cv.destroyAllWindows()

#--------------------------------------------------Mouse Click Event (1)--------------------------------------------------#

img = cv.imread('R.jpg')

def click_position(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        # Correct BGR indexing: img[row, col] -> img[y, x]
        blue = img[y, x, 0]
        green = img[y, x, 1]
        red = img[y, x, 2]
        
        # Create a display window for the color
        imgcolor = np.zeros([500, 500, 3], np.uint8)
        imgcolor[:] = [blue, green, red]
        

        color_text = f"BGR: ({blue}, {green}, {red})"
        cv.putText(imgcolor, color_text, (50, 250), 
                   cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        cv.imshow("Selected Color", imgcolor)

# Create a named window first so the callback attaches correctly
cv.namedWindow('Color Picker')
cv.setMouseCallback('Color Picker', click_position)

while True:
    cv.imshow('Color Picker', img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()

#--------------------------------------------------Mouse Click Event (2)--------------------------------------------------#

#Show cord when pressed and link all pressed dots

img = cv.imread('R.jpg')
points = []

def click_position(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:

        blue = img[y, x, 0]
        green = img[y, x, 1]
        red = img[y, x, 2]
        
        color_text = f"R:G:B={red},{green},{blue}"
        
        cv.circle(img, (x, y), 10, (0, 255, 0), 5)
        
        points.append((x, y))
        if len(points) >= 2:
            # Draw a red line between the last two points
            cv.line(img, points[-1], points[-2], (0, 0, 255), 3)

        cv.putText(img, color_text, (x, y - 15), 1, 1.5, (255, 255, 255), 2)
        
        # Refresh the window
        cv.imshow('Interactive Window', img)

cv.imshow('Interactive Window', img)
cv.setMouseCallback('Interactive Window', click_position)
cv.waitKey(0)
cv.destroyAllWindows()

#--------------------------------------------------Mouse Click Event (3)--------------------------------------------------#

#Draw a rectangle shape by every i random a new color.

# Create a black square canvas (600x600 pixels, 3 color channels)
img = np.zeros((600,600,3), dtype=np.uint8)
drawing = False      # Becomes True when you press the left button
ix, iy = -1, -1      # Starting (initial) x, y coordinates
ex, ey = -1, -1      # Ending (current) x, y coordinates

# Pick a random color in BGR format (Blue, Green, Red)
current_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255)) 

def click_position(event, x, y, flags, param):
    global ix, iy, ex, ey, drawing, current_color

    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y  # Lock the starting point
        ex, ey = x, y  # Initialize the end point at the start point
        current_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255)) 

    elif event == cv.EVENT_MOUSEMOVE:
        if drawing:    
            ex, ey = x, y  

    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        ex, ey = x, y
        # PERMANENTLY draw the final rectangle onto the 'img' canvas
        cv.rectangle(img, (ix, iy), (ex, ey), current_color, 2)

cv.namedWindow("homework")
cv.setMouseCallback("homework", click_position)


while True:
    display_img = img.copy() 
    if drawing:
        cv.rectangle(display_img, (ix, iy), (ex, ey), current_color, 2)
    cv.imshow("homework", display_img)
    # If 'ESC' (key 27) is pressed, close the program
    if cv.waitKey(10) == 27:  
        break

cv.destroyAllWindows()



#--------------------------------------------------Bitwise &  Color (0)--------------------------------------------------#

# Create two white canvases (500x500 pixels, 3 channels, 8-bit)
img1 = np.full((500,500,3), 255, dtype=np.uint8)
img2 = np.full((500,500,3), 255, dtype=np.uint8)
img3 = cv.imread('R.jpg') # Load your source image

# --- 2. COLOR FILTERING (HSV/BGR Thresholding) ---
# Define the range of BGR value green color to detect 
upper_green = np.array([100, 255, 130]) #dark green
lower_green = np.array([0, 50, 0]) # mint green

# Create a binary mask: white pixels = green detected, black pixels = everything else
mask = cv.inRange(img3, lower_green, upper_green)

# Apply the mask: only keep pixels where the mask is white (the green parts)
result = cv.bitwise_and(img3, img3, mask=mask)

# --- 3. DRAWING SHAPES FOR LOGIC TESTING ---
# Draw a blue-ish rectangle on img1 and a circle on img2
cv.rectangle(img1, (70, 70), (430, 430), (245, 160, 118), -1)
cv.circle(img2, (250, 250), 200, (245, 160, 118), -1)

# --- 4. BITWISE OPERATIONS ---
# Intersection: Only shows area where both shapes overlap
bitwise_and = cv.bitwise_and(img1, img2)

# Union: Shows the combined area of both shapes
bitwise_or = cv.bitwise_or(img1, img2) 

# Inversion: Flips the colors of img1 (Black -> white)
# If a pixel is White (255), NOT makes it Black (0)
# If a pixel is 200, NOT makes it 55 (255 - 200)
bitwise_not = cv.bitwise_not(img1)

# Difference: Shows only areas where the shapes DO NOT overlap
bitwise_xor = cv.bitwise_xor(img1, img2)

# --- 5. DISPLAY RESULTS ---
cv.imshow('Rectangle', img1)
cv.imshow('circle', img2)
cv.imshow('AND', bitwise_and)
cv.imshow('OR', bitwise_or)
cv.imshow('NOT', bitwise_not)
cv.imshow('XOR', bitwise_xor)
cv.imshow('origin', img3)
cv.imshow('detect color mask', mask)
cv.imshow('result', result)

cv.waitKey(0)
cv.destroyAllWindows()

#--------------------------------------------------Bitwise &  Color (1)--------------------------------------------------#

# HSV and masking from Cam

# Initialize the webcam (0 is usually the default built-in camera)
cap = cv.VideoCapture(0)

# 1. DEFINE COLOR THRESHOLDS
# We use HSV (Hue, Saturation, Value) because it is more robust to lighting changes.
# Format: [Hue (0-179), Saturation (0-255), Value (0-255)]
colors = {
    "Green": (np.array([35, 60, 40]), np.array([85, 255, 255])),
    "Gray":  (np.array([0, 0, 50]), np.array([180, 30, 200])),
    "White": (np.array([0, 0, 200]), np.array([180, 30, 255]))
}

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    # Capture frame-by-frame from the webcam
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # 2. DEFINE REGION OF INTEREST (ROI)
    # This limits detection to a specific box to save processing power.
    # roi_coords is for drawing: (x1, y1, x2, y2)
    roi_coords = (180, 10, 400, 450) 
    

    cv.rectangle(frame, (roi_coords[0], roi_coords[1]), (roi_coords[2], roi_coords[3]), (0, 255, 0), 2)
    
    # Crop the image: frame[y_start:y_end, x_start:x_end]
    roi = frame[10:450, 180:400]
    
    # 3. COLOR CONVERSION
    # Convert the cropped BGR image from the camera into the HSV color space
    hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)

    # 4. ITERATIVE COLOR FILTERING
    for name, (lower, upper) in colors.items():
        
        # Create a Mask: Pixels inside the range become White (255), outside become Black (0)
        mask = cv.inRange(hsv_roi, lower, upper)
        
        # Bitwise AND: Keep only the pixels from the 'roi' where the 'mask' is White.
        # This effectively hides everything except the detected color.
        result = cv.bitwise_and(roi, roi, mask=mask)
        
        # Show a separate window for each color (Green LEGO, Gray LEGO, etc.)
        cv.imshow(f'{name} LEGO', result)

    cv.imshow('Original (with ROI box)', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

#--------------------------------------------------Mathplot (0)--------------------------------------------------#

x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

plt.plot(x, y, label='Growth', color='blue', marker='o')
plt.title("Simple Line Plot")
plt.xlabel("X-Axis")
plt.ylabel("Y-Axis")
plt.legend()
plt.show()

#--------------------------------------------------Mathplot (1)--------------------------------------------------#

#subplot

img = cv.imread('R.jpg')

# 2. Create the first subplot in a 1x3 grid
# Arguments: (rows, columns, index)
# 'title' sets the label above the image.
# 'xticks' and 'yticks' are set to empty lists [] to hide the pixel coordinate scales.
plt.subplot(1, 3, 1, title=" BGR ", xticks=[], yticks=[])

# Matplotlib expects RGB (Red-Green-Blue).
# Because 'img' is currently BGR, the Blue and Red channels are swapped, 
# making people look blue/orange.
plt.imshow(img)

# 3. Use NumPy Slicing to fix color on the fly
# plt.subplot(1, 3, 2) moves to the middle position.
plt.subplot(1, 3, 2, title=" RGB ", xticks=[], yticks=[])

# Slicing explained: [rows, columns, channels]
# [:, :, ::-1] means: take all rows, all columns, but reverse the 3rd dimension.
# This flips index 0 (Blue) with index 2 (Red), resulting in RGB.
plt.imshow(img[:, :, ::-1])

# 4. Use OpenCV's built-in conversion function
# This is the "standard" way to convert color spaces in computer vision projects.
# cv.COLOR_BGR2RGB is a flag that tells the function how to remap the array.
img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

# Select the third position in the grid.
plt.subplot(1, 3, 3, title=" RGB cvt ", xticks=[], yticks=[])

plt.imshow(img_rgb)

plt.show()

#--------------------------------------------------Mathplot (2)--------------------------------------------------#

#Gray Mask
# Load the image and convert it to grayscale
img = cv.imread("R.jpg")
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# Get dimensions and create a blank canvas for the thresholded image
x, y = img.shape[:2]
imgth = np.zeros([x, y], np.uint8)

# Manual thresholding logic
for i in range(x):
    for j in range(y):
        # verify if both i and j have the brightness over 128
        #If the pixel is darker than the midpoint (128), it sets the new image pixel (imgth) to 0 (Black).
        #If the pixel is 128 or brighter, it sets it to 1 (White).
        if img[i, j] < 128:
            imgth[i, j] = 0
        elif img[i, j] >= 128:
            imgth[i, j] = 1

# Display the result
plt.imshow(imgth, cmap="gray")
plt.show()

#--------------------------------------------------Mathplot (3)--------------------------------------------------#

#threshold

original_img = cv.imread("R.jpg")

# 2. CONVERT TO GRAYSCALE
# Thresholding only works on single-channel images (grayscale).
# If the image fails to load, original_img will be None.
if original_img is None:
    print("Error: Could not find 'R.jpg'. Check the file path.")
else:
    gray_img = cv.cvtColor(original_img, cv.COLOR_BGR2GRAY)

    # 3. DEFINE THRESHOLD VALUES
    # These are the 'cutoff' points. 
    # Lower values (75) let more light in; higher values (230) make it stricter.
    # Simply put, lower thresholds yield lighter images, higher thresholds yield darker images.
    thresh_values = [75, 100, 128, 180, 230]

    # Set up the display window size
    plt.figure(figsize=(15, 8))

    for i, val in enumerate(thresh_values):
        
        # cv.threshold logic:
        # If a pixel is brighter than 'val', it becomes 255 (White).
        # If it is darker, it becomes 0 (Black).
        # '_' is a placeholder for the first return value which we don't need here.
        _, result = cv.threshold(gray_img, val, 255, cv.THRESH_BINARY)
        
        # 5. CREATE SUBPLOTS
        # This organizes the images in a grid. 
        # 231 means: 2 rows, 3 columns, and this is position 'i + 1'
        plt.subplot(2, 3, i + 1)
        
        # Add a title to each image to show the threshold used
        plt.title(f"Threshold: {val}")
        
        # Hide the X and Y graph coordinates for a cleaner look
        plt.xticks([]), plt.yticks([])
        
        # Display the result
        plt.imshow(result, cmap="gray")

    # 6. SHOW THE ORIGINAL AS THE LAST PLOT
    # This helps you compare the results to the source image
    plt.subplot(2, 3, 6)
    plt.title("Original Gray")
    plt.xticks([]), plt.yticks([])
    plt.imshow(gray_img, cmap="gray")

    # Adjust layout so titles don't overlap and show the window
    plt.tight_layout()
    plt.show()

#--------------------------------------------------Mathplot (4)--------------------------------------------------#

#threshold types

# Load the image and immediately convert it to grayscale
img = cv.imread("R.jpg")
gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

thresh_values = [75, 100, 128, 180, 230]

plt.figure(figsize=(15, 10))

for i in range(len(thresh_values)):
    # cv.threshold(src, thresh, maxval, type)
    # Pixels > thresh become 255 (white); others become 0 (black)
    _, result = cv.threshold(gray_img, thresh_values[i], 255, cv.THRESH_BINARY)
    
    # Create a subplot for each simple threshold result
    plt.subplot(3, 3, i + 1)
    plt.title("Simple Thresh: %d" % thresh_values[i])
    plt.xticks([]), plt.yticks([]) 
    plt.imshow(result, cmap="gray")

# 3. ADAPTIVE THRESHOLDING (From your second and third ref)
# Unlike simple thresholding, these methods calculate the cutoff locally for each block

# Method A: Adaptive Mean
# Calculates threshold based on the average of the block area
res_mean = cv.adaptiveThreshold(gray_img, 255, cv.ADAPTIVE_THRESH_MEAN_C, 
                                cv.THRESH_BINARY, 11, 2)

# Method B: Adaptive Gaussian
# Calculates threshold based on a weighted sum of the block area (often cleaner)
res_gauss = cv.adaptiveThreshold(gray_img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                 cv.THRESH_BINARY, 11, 2)

# 4. DISPLAY ADAPTIVE RESULTS
# Show Adaptive Mean in position 7
plt.subplot(3, 3, 7)
plt.title("Adaptive Mean")
plt.xticks([]), plt.yticks([])
plt.imshow(res_mean, cmap="gray")

# Show Adaptive Gaussian in position 8
plt.subplot(3, 3, 8)
plt.title("Adaptive Gauss")
plt.xticks([]), plt.yticks([])
plt.imshow(res_gauss, cmap="gray")

# Show Original Grayscale in position 9 for comparison
plt.subplot(3, 3, 9)
plt.title("Original Gray")
plt.xticks([]), plt.yticks([])
plt.imshow(gray_img, cmap="gray")

plt.tight_layout()
plt.show()

#--------------------------------------------------Morphological--------------------------------------------------#

# Coin Counter

# value of each coin in terms of range
coin_values = {
    '1': {'min': 27, 'max': 28, 'value': 1},
    '2': {'min': 29, 'max': 33, 'value': 2},
    '10': {'min': 34, 'max': 40, 'value': 10}
}

def classify_coin(radius):
    for label, info in coin_values.items():
        # check the min and max radius based on the dict 
        # Label = 1,2,10 | info = min max value
        if info['min'] <= radius <= info['max']:
            return label
    return None

# Load the video file
cap = cv.VideoCapture('m5python/Aj phoom-my work/023546_school/coinn.mp4')
previous_coins = {}

# Smooting the pic 
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5)) 

while True:
    ret, frame = cap.read()
    if not ret:
        break

    #Pre-processing set up
    roi = frame[:1080, 0:1920]  # Define Region of Interest
    gray = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)  # Convert to Grayscale
    blur = cv.GaussianBlur(gray, (11, 11), 0)   # Smooth image to reduce noise-
    
    # Use Otsu's Thresholding to create a binary (black & white) image
    _, thresh = cv.threshold(blur, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

    # Morphology: Clean up the binary image
    opened = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=1) # remove small noise
    closed = cv.morphologyEx(opened, cv.MORPH_CLOSE, kernel, iterations=2) # fill in hole in white

    # Contour Detection: Find the shapes of the coins
    contours, _ = cv.findContours(closed.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    coins = {}
    total_value = 0
    coin_count = 0

    for cnt in contours:
        area = cv.contourArea(cnt)
        # Filter out contours that are too small or too large to be coins
        if area < 1000 or area > 40000:
            continue

        # Get the center (x, y) and radius of the minimum circle that fits the contour
        (x, y), radius = cv.minEnclosingCircle(cnt)
        radius = int(radius)
        coin_type = classify_coin(radius)

        if coin_type is not None:
            # Create a basic ID based on grid position to track the coin across frames
            coin_id = f"{int(x // 10)}_{int(y // 10)}"  
            coins[coin_id] = (coin_type, (int(x), int(y), radius))

    # 4. Smoothing/Filtering: Compare with previous frame to reduce flickering
    smoothed_coins = {}
    for cid, data in coins.items():
        if cid in previous_coins or len(previous_coins) == 0:
            smoothed_coins[cid] = data
            total_value += coin_values[data[0]]['value']
            coin_count += 1

    # 5. Visualization: Draw circles and text on the frame
    for coin_type, (x, y, radius) in smoothed_coins.values():
        cv.circle(roi, (x, y), radius, (20, 255, 57), 2) # Green circle
        cv.putText(roi, f"{coin_type}B", (x - 10, y), 
                   cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Overlay the total count and value on the screen
    cv.putText(roi, f"Coins: {coin_count}", (50, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (204, 50, 153), 3)
    cv.putText(roi, f"Total: {total_value} Baht", (50, 170), cv.FONT_HERSHEY_SIMPLEX, 1, (128, 128, 240), 3)

    cv.imshow("Coin Counter", roi)
    
    # Calculate delay to match video FPS
    fps = cap.get(cv.CAP_PROP_FPS)
    delay = int(1000 / (fps * 1))

    previous_coins = coins.copy()

    # Press 'q' to exit the loop
    if cv.waitKey(delay) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()


import cv2 as cv
import os

#--------------------------------------------------Face Detection (img)--------------------------------------------------#

img = cv.imread("m5python/Reverse Engineering/IMG_2126.JPG")

def rescaleFrame(frame,scale=0.5):
    width = int(frame.shape[1]*scale)
    height = int(frame.shape[0]*scale)
    dimensions = (width,height)
    return cv.resize(frame,dimensions,interpolation=cv.INTER_AREA)

frame_resized = rescaleFrame(img)

xml_path = cv.data.haarcascades + 'haarcascade_frontalface_default.xml'

# Initialize the Face Cascade Classifier
face_cascde = cv.CascadeClassifier(xml_path)
gray_img = cv.cvtColor(frame_resized, cv.COLOR_RGB2GRAY)

# Parameters for face detection:
# scale: How much the image size is reduced at each image scale
# minNeighbor: How many neighbors each candidate rectangle should have to retain it
scale = 1.1
minNeighbor = 3
face_detect = face_cascde.detectMultiScale(gray_img, scale, minNeighbor)
if len(face_detect) > 0:
    for x, y, w, h in face_detect:
        cv.rectangle(frame_resized, (x, y), (x + w, y + h), (0, 255, 0), 2)
else:
    print("No faces detected.")

cv.imshow("Face detect",frame_resized)
cv.waitKey(0)
cv.destroyAllWindows()

#--------------------------------------------------Face Detection (live cam)--------------------------------------------------#
cap = cv.VideoCapture(0)
xml_path = cv.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascde = cv.CascadeClassifier(xml_path)

while (cap.isOpened()):
    chack, frame = cap.read()
    
    if chack:
        gray_cap = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
        face_detect = face_cascde.detectMultiScale(gray_cap)
        for (x, y, w, h) in face_detect:
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)
        cv.imshow("face detect", frame)
        if cv.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if no frame is received (end of video or camera error)
        break

# Remember to release the capture and close windows when done
cap.release()
cv.destroyAllWindows()

#--------------------------------------------------Eye Detection (pic)--------------------------------------------------#

img = cv.imread("C:/Users/LENOVO/Documents/Lieutenant Hecker/Primary Data\Digital Data/77745.jpg")

xml_path = cv.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml'
eye_cascde = cv.CascadeClassifier(xml_path)

gray_img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

scale = 1.1
minNeighbor = 10
eye_detect = eye_cascde.detectMultiScale(gray_img, scale, minNeighbor)

print(eye_detect)
for (x, y, w, h) in eye_detect:
    cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), thickness=2)

cv.imshow("eye detect", img)
cv.waitKey(0)
cv.destroyAllWindows()

import cv2 as cv
import os

if not os.path.exists("captured_faces"):
    os.makedirs("captured_faces")

cap = cv.VideoCapture(0)
xml_path = cv.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv.CascadeClassifier(xml_path)
clf = cv.face.LBPHFaceRecognizer_create()
clf.read("classifier.xml")

names = {
    5: "N/A"
}

ret, frame1 = cap.read()

while True:
    ret, frame1 = cap.read()
    if not ret: break

    gray_img = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
    face_detect = face_cascade.detectMultiScale(gray_img, 1.1, 5)
    for (x, y, w, h) in face_detect:
        face_img = gray_img[y:y + h, x:x + w]
        id, con = clf.predict(face_img)
        name = names.get(id, "unknown")
        label = f"{name} ({id})"
        cv.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv.putText(frame1, label, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv.imshow("Face & Motion Detection", frame1)
    if cv.waitKey(33) & 0xFF == ord('q'):
        break
    continue

cap.release()
cv.destroyAllWindows()
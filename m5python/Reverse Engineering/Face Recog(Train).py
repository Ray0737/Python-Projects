import numpy as np
from PIL import Image
import os
import cv2

def train_classifier(data_dir):
    # Get all file paths in the directory
    path = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    faces = []
    ids = []
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    for image_path in path:
        # Open image and convert to grayscale
        img = Image.open(image_path).convert("L")
        imageNp = np.array(img, 'uint8')
        
        # Extract ID from file name (Assuming format: user.1.png)
        try:
            id = int(os.path.split(image_path)[1].split(".")[1])
        except (IndexError, ValueError):
            print(f"Skipping {image_path}: Filename format must be 'name.id.extension'")
            continue

        # Detect faces in the training image
        detected_faces = face_cascade.detectMultiScale(imageNp)
        
        for (x, y, w, h) in detected_faces:
            faces.append(imageNp[y:y+h, x:x+w]) # Crop to the face only
            ids.append(id)

    # Convert ids to numpy array
    ids = np.array(ids)

    # Initialize and train the LBPH Face Recognizer
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces, ids)
    clf.write("classifier.xml")
    print("Training Completed! Model saved as classifier.xml")

# Run the training
train_classifier('data')
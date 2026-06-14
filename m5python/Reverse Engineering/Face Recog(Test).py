import cv2 as cv
import os
import time

# --- Initialization ---
# Create directory to save face images if it doesn't exist
if not os.path.exists("captured_faces"):
    os.makedirs("captured_faces")

cap = cv.VideoCapture(0) # Open the default camera

# Load the face detection model (Haar Cascade)
xml_path = cv.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv.CascadeClassifier(xml_path)

# Load the face RECOGNITION model (trained on specific faces)
clf = cv.face.LBPHFaceRecognizer_create()
clf.read("classifier.xml") # This file must exist from your training script

# Database of IDs and Names
names = {1: "Gain"}

# --- Motion Detection Buffers ---
# We read two frames to compare the difference between them
ret, frame1 = cap.read()
ret, frame2 = cap.read()

filled_ids = set() # Stores IDs of people who moved

# --- Countdown Logic ---
countdown_secs = 10
start_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret: break

    elapsed = int(time.time() - start_time)
    gray_img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) # Convert to gray for processing
    
    # Detect all faces in the current frame
    face_detect = face_cascade.detectMultiScale(gray_img, 1.1, 5)

    # --- PHASE 1: The Countdown (Safe Period) ---
    if elapsed < countdown_secs:
        remaining = countdown_secs - elapsed
        cv.putText(frame, f"Countdown: {remaining}s", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
        
        for (x, y, w, h) in face_detect:
            # Recognize the face
            face_roi = gray_img[y:y + h, x:x + w]
            id, con = clf.predict(face_roi)
            name = names.get(id, "unknown")
            
            # Draw green box (Safe)
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv.putText(frame, f"{name} ({id})", (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        cv.imshow("Face & Motion Detection", frame)
        frame1 = frame2
        ret, frame2 = cap.read()
        if cv.waitKey(33) & 0xFF == ord('q'): break
        continue

    # --- PHASE 2: Motion Detection (The Game) ---
    # 1. Calculate the difference between consecutive frames
    motiondiff = cv.absdiff(frame1, frame2)
    gray_motion = cv.cvtColor(motiondiff, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray_motion, (5, 5), 0) # Reduce noise
    
    # 2. Thresholding: Turn movement into white pixels, static into black
    _, result = cv.threshold(blur, 50, 255, cv.THRESH_BINARY)
    dilation = cv.dilate(result, None, iterations=3) # Make moving areas "thicker"
    
    # 3. Find contours (the outlines of moving objects)
    contours, _ = cv.findContours(dilation, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

    for (x, y, w, h) in face_detect:
        face_roi = gray_img[y:y + h, x:x + w]
        id, con = clf.predict(face_roi)
        
        # Determine if any movement contour is inside the face rectangle
        moving = False
        for contour in contours:
            cx, cy, cw, ch = cv.boundingRect(contour)
            if cv.contourArea(contour) < 2500: continue # Ignore tiny movements
            
            # Collision detection: Does the moving box touch the face box?
            if (x < cx + cw and x + w > cx and y < cy + ch and y + h > cy):
                moving = True
                break

        if moving:
            filled_ids.add(id) # Mark this person as "out" or "caught"

        # Visual feedback: Red solid box if moved, Green outline if still
        if id in filled_ids:
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), -1) # -1 means fill
        else:
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # --- Winner Logic ---
    all_ids = {clf.predict(gray_img[y:y+h, x:x+w])[0] for (x, y, w, h) in face_detect}
    
    # If only one person hasn't moved yet, they are the winner
    if len(all_ids) - len(filled_ids) == 1 and len(filled_ids) >= 1:
        winner_ids = all_ids - filled_ids
        if winner_ids:
            winner_name = names.get(list(winner_ids)[0], "unknown")
            cv.putText(frame, f"{winner_name} wins!", (50, 100), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 4)

    cv.imshow("Face & Motion Detection", frame)
    frame1 = frame2
    ret, frame2 = cap.read()
    if cv.waitKey(33) & 0xFF == ord('q'): break

cap.release()
cv.destroyAllWindows()
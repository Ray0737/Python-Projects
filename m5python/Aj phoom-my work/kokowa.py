import cv2
import os
import time

# --- Setup ---
if not os.path.exists("captured_faces"):
    os.makedirs("captured_faces")
# --- Setup face recog---
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
# --- Setup Model---
clf = cv2.face.LBPHFaceRecognizer_create()
clf.read("four.xml")

names = {
    1: "mark",
    2: "august",
    3: "the black one",
    4: "zen"
}

# --- Motion detection setup ---
ret, frame1 = cap.read()
ret, frame2 = cap.read()

filled_ids = set()

# --- Countdown setup ---
countdown_secs = 10
start_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    elapsed = int(time.time() - start_time) # Current time
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_detect = face_cascade.detectMultiScale(gray_img, 1.1, 5) # Detection

    if elapsed < countdown_secs:
        # Show countdown on frame
        remaining = countdown_secs - elapsed
        cv2.putText(frame, f"Countdown: {remaining}s", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
        # Draw green boxes and labels only
        for (x, y, w, h) in face_detect:
            face_img = gray_img[y:y + h, x:x + w]
            id, con = clf.predict(face_img)
            name = names.get(id, "unknown")
            label = f"{name} ({id})"
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.imshow("Face & Motion Detection", frame)
        frame1 = frame2
        ret, frame2 = cap.read()
        if cv2.waitKey(33) & 0xFF == ord('q'):
            break
        continue

    # --- Motion detection ---
    motiondiff = cv2.absdiff(frame1, frame2)
    gray_motion = cv2.cvtColor(motiondiff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray_motion, (5, 5), 0)
    _, result = cv2.threshold(blur, 50, 255, cv2.THRESH_BINARY)
    dilation = cv2.dilate(result, None, iterations=3)
    contours, _ = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for (x, y, w, h) in face_detect:
        face_img = gray_img[y:y + h, x:x + w]
        id, con = clf.predict(face_img)
        name = names.get(id, "unknown")
        label = f"{name} ({id})"

        # Check for movement in the face region
        moving = False
        for contour in contours:
            cx, cy, cw, ch = cv2.boundingRect(contour)
            if cv2.contourArea(contour) < 2500:
                continue
            if (x < cx + cw and x + w > cx and y < cy + ch and y + h > cy):
                moving = True
                break

        # Only add this id if this face moved
        if moving:
            filled_ids.add(id)

        # Only fill the bounding box for this id if it has moved
        if id in filled_ids:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), -1)
        else:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Find all unique IDs in the current frame
    all_ids = set()
    for (x, y, w, h) in face_detect:
        face_img = gray_img[y:y + h, x:x + w]
        id, con = clf.predict(face_img)
        all_ids.add(id)

    # If all but one face have filled boxes, declare the last as winner
    if len(all_ids) - len(filled_ids) == 1 and len(filled_ids) >= 1:
        winner_ids = all_ids - filled_ids
        if winner_ids:
            winner_id = winner_ids.pop()
            winner_name = names.get(winner_id, "unknown")
            win_text = f"{winner_name} wins the game!"
            cv2.putText(frame, win_text, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 4)

    cv2.imshow("Face & Motion Detection", frame)
    frame1 = frame2
    ret, frame2 = cap.read()
    if cv2.waitKey(33) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
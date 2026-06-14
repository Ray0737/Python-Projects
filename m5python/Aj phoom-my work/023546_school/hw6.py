import cv2 as cv

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

cap = cv.VideoCapture("coinn.mp4")
previous_coins = {}

kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    roi = frame[:1080, 0:1920]
    gray = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (11, 11), 0)
    _, thresh = cv.threshold(blur, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

    opened = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=1)
    closed = cv.morphologyEx(opened, cv.MORPH_CLOSE, kernel, iterations=2)

    contours, _ = cv.findContours(closed.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    coins = {}
    total_value = 0
    coin_count = 0

    for cnt in contours:
        area = cv.contourArea(cnt)
        if area < 1000 or area > 40000:
            continue

        (x, y), radius = cv.minEnclosingCircle(cnt)
        radius = int(radius)
        coin_type = classify_coin(radius)

        if coin_type is not None:
            coin_id = f"{int(x // 10)}_{int(y // 10)}"  
            coins[coin_id] = (coin_type, (int(x), int(y), radius))

    smoothed_coins = {}
    for cid, data in coins.items():
        if cid in previous_coins or len(previous_coins) == 0:
            smoothed_coins[cid] = data
            total_value += coin_values[data[0]]['value']
            coin_count += 1

    for coin_type, (x, y, radius) in smoothed_coins.values():
        cv.circle(roi, (x, y), radius, (20,255,57), 2)
        cv.putText(roi, f"{coin_type}B", (x - 10, y), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv.putText(roi, f"Coins: {coin_count}", (50, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (204,50,153), 3)
    cv.putText(roi, f"Total: {total_value} Baht", (50, 170), cv.FONT_HERSHEY_SIMPLEX, 1, (128,128,240), 3)

    cv.imshow("Coin Counter", roi)
    fps = cap.get(cv.CAP_PROP_FPS)
    delay = int(1000 / (fps * 1))

    previous_coins = coins.copy()

    if cv.waitKey(delay) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

import cv2
import requests
import time

# ==============================
# SETTINGS
# ==============================
ESP_IP = "192.168.1.45"   # 🔁 CHANGE THIS
MAX_LIMIT = 3             # 🔁 Change limit here
CONF_THRESHOLD = 0.6

# ==============================
# LOAD FACE MODEL
# ==============================
modelFile = "res10_300x300_ssd_iter_140000_fp16.caffemodel"
configFile = "deploy.prototxt"

net = cv2.dnn.readNetFromCaffe(configFile, modelFile)

cap = cv2.VideoCapture(0)

last_command = ""
last_send_time = 0
SEND_DELAY = 2   # seconds (prevents spamming ESP32)

print("System Started...")
print("Press Q to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]

    blob = cv2.dnn.blobFromImage(
        frame,
        1.0,
        (300, 300),
        (104.0, 177.0, 123.0)
    )

    net.setInput(blob)
    detections = net.forward()

    face_count = 0

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > CONF_THRESHOLD:
            face_count += 1

            box = detections[0, 0, i, 3:7] * [w, h, w, h]
            (x1, y1, x2, y2) = box.astype("int")

            cv2.rectangle(frame, (x1, y1), (x2, y2),
                          (0, 255, 0), 2)

    # ==============================
    # GATE LOGIC (WIRELESS)
    # ==============================
    current_time = time.time()

    if face_count >= MAX_LIMIT:
        command = "CLOSE"
        status = "ENTRY CLOSED"
        url = f"http://{ESP_IP}/close"
    else:
        command = "OPEN"
        status = "ENTRY OPEN"
        url = f"http://{ESP_IP}/open"

    # Send only if command changed OR delay passed
    if (command != last_command) or (current_time - last_send_time > SEND_DELAY):
        try:
            requests.get(url, timeout=1)
            print(f"Sent: {command}")
            last_command = command
            last_send_time = current_time
        except:
            print("ESP32 not reachable")

    # ==============================
    # DISPLAY INFO
    # ==============================
    cv2.putText(frame, f"Face Count: {face_count}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                3)

    cv2.putText(frame, status,
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),
                3)

    cv2.imshow("Wireless Crowd Management", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

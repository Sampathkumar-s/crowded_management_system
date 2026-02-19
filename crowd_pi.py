import cv2
import serial
import time

# -------- Serial Setup --------
esp = serial.Serial('COM5', 115200)  # Change COM port
time.sleep(2)

MAX_LIMIT = 3  # Max allowed people

# -------- Load Face Model --------
modelFile = "res10_300x300_ssd_iter_140000_fp16.caffemodel"
configFile = "deploy.prototxt"

net = cv2.dnn.readNetFromCaffe(configFile, modelFile)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]

    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
                                 (104.0, 177.0, 123.0))

    net.setInput(blob)
    detections = net.forward()

    face_count = 0

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > 0.6:
            face_count += 1

            box = detections[0, 0, i, 3:7] * [w, h, w, h]
            (x1, y1, x2, y2) = box.astype("int")

            cv2.rectangle(frame, (x1, y1), (x2, y2),
                          (0, 255, 0), 2)

    # -------- Gate Logic --------
    if face_count >= MAX_LIMIT:
        esp.write(b"CLOSE\n")
        status = "ENTRY CLOSED"
    else:
        esp.write(b"OPEN\n")
        status = "ENTRY OPEN"

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

    cv2.imshow("Face Counter System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
esp.close()
cv2.destroyAllWindows()

import cv2
from ultralytics import YOLO

# Load face detection model
model = YOLO("yolov8n-face.pt")  # automatically downloads

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    face_count = 0

    for r in results:
        for box in r.boxes:
            conf = float(box.conf[0])
            if conf > 0.5:
                face_count += 1
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)

    cv2.putText(frame, f"Face Count: {face_count}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,0,255),
                3)

    cv2.imshow("High Accuracy YOLO Face Counter", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

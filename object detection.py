import cv2
import torch
import numpy as np
import pyttsx3
import threading
import time

# === Initialize Text-to-Speech Engine (INSTANT SPEECH) === #
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 180)  # Slightly faster speech

def speak(text):
    """Speaks the detected objects IMMEDIATELY using a separate thread."""
    threading.Thread(target=lambda: tts_engine.say(text) or tts_engine.runAndWait(), daemon=True).start()

# === Load YOLOv5 Model for Object Detection === #
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.conf = 0.5  # Confidence threshold

# === Load QR Code Detector === #
qr_detector = cv2.QRCodeDetector()

# === Open Webcam === #
video = cv2.VideoCapture(1)
video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# === Track Last Spoken Items to Avoid Repetitions === #
last_spoken = {}
speech_cooldown = 4  # 3 sec delay before repeating the same detection

while True:
    ret, frame = video.read()
    if not ret:
        break

    current_time = time.time()

    # === STEP 1: QR CODE DETECTION === #
    qr_data, bbox, _ = qr_detector.detectAndDecode(frame)
    if qr_data and ("QR" not in last_spoken or (current_time - last_spoken["QR"]) > speech_cooldown):
        speak(f"QR Code detected: {qr_data}")
        last_spoken["QR"] = current_time
        cv2.putText(frame, f"QR: {qr_data}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        if bbox is not None:
            bbox = np.int32(bbox)
            cv2.polylines(frame, [bbox], True, (255, 0, 0), 2)

    # === STEP 2: OBJECT DETECTION === #
    results = model(frame)
    detected_objects = [results.names[int(cls)] for *box, conf, cls in results.xyxy[0]]

    # Count detected objects
    object_counts = {obj: detected_objects.count(obj) for obj in set(detected_objects)}

    # Convert counts to singular/plural properly
    object_speech = []
    for obj, count in object_counts.items():
        obj_text = f"{count} {obj}" if count > 1 else obj  # "2 persons" or "person"
        
        if obj not in last_spoken or (current_time - last_spoken[obj]) > speech_cooldown:
            object_speech.append(obj_text)
            last_spoken[obj] = current_time  # Update last spoken time

    # Speak detected objects IMMEDIATELY
    if object_speech:
        speak(", ".join(object_speech))

    # Draw bounding boxes for detected objects
    for *box, conf, cls in results.xyxy[0]:
        x1, y1, x2, y2 = map(int, box)
        label = results.names[int(cls)]
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # === Show Output === #
    cv2.imshow("AI Glasses - Object & QR Mode", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# === Cleanup === #
video.release()
cv2.destroyAllWindows()

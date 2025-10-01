import cv2
import torch
import numpy as np
import pyttsx3
from pathlib import Path
import sys
import time

from collections import Counter

# TTS Setup
tts = pyttsx3.init()
tts.setProperty('rate', 150)
def speak(text):
    print("[Audio]:", text)
    tts.say(text)
    tts.runAndWait()

# Load YOLOv5s
sys.path.append(str(Path("yolov5").resolve()))
yolo = torch.hub.load('ultralytics/yolov5', 'yolov5s', trust_repo=True).to("cuda" if torch.cuda.is_available() else "cpu")
yolo.eval()

cap = cv2.VideoCapture(1)

# Variables to manage cooldown
last_speak_time, last_message = 0, ""
repeat_cooldown = 10  # seconds

# For last few frames message to avoid repeats
message_buffer = []

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    zone_width = w // 3
    zones = {"left": [], "center": [], "right": []}

    # Inference
    results = yolo(frame)
    detections = results.xyxy[0].cpu().numpy()

    for det in detections:
        x1, y1, x2, y2, conf, cls = map(int, det[:6])
        cx = (x1 + x2) // 2
        box_h = y2 - y1
        label = results.names[int(cls)]

        # Estimate proximity
        if box_h > 250:
            proximity = "very close"
        elif box_h > 150:
            proximity = "close"
        else:
            proximity = "far"

        # Determine zone
        if cx < zone_width:
            zone = "left"
        elif cx > 2 * zone_width:
            zone = "right"
        else:
            zone = "center"

        zones[zone].append((label, proximity))
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(frame, f"{label} ({proximity})", (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    # Decide what to speak
    message = "Clear path ahead"
    if zones["center"]:
        obj, prox = sorted(zones["center"], key=lambda x: ["far", "close", "very close"].index(x[1]))[0]
        direction = "left" if len(zones["left"]) < len(zones["right"]) else "right"
        message = f"{obj.capitalize()} {prox} ahead, move {direction}"
    elif zones["left"]:
        obj, prox = sorted(zones["left"], key=lambda x: ["far", "close", "very close"].index(x[1]))[0]
        message = f"{obj.capitalize()} on left, {prox}, move center or right"
    elif zones["right"]:
        obj, prox = sorted(zones["right"], key=lambda x: ["far", "close", "very close"].index(x[1]))[0]
        message = f"{obj.capitalize()} on right, {prox}, move center or left"

    # Speak only if:
    # 1. The message is new
    # 2. Cooldown time has passed
    # 3. It’s not a quick repetition from previous few frames
    now = time.time()
    if (message != last_message and message not in message_buffer) or (now - last_speak_time > repeat_cooldown):
        speak(message)
        last_message = message
        last_speak_time = now
        message_buffer.append(message)
        if len(message_buffer) > 5:  # keep only last few messages
            message_buffer.pop(0)

    # Draw guidance zones
    cv2.line(frame, (zone_width, 0), (zone_width, h), (0, 255, 0), 2)
    cv2.line(frame, (2 * zone_width, 0), (2 * zone_width, h), (0, 255, 0), 2)

    cv2.imshow("Indoor Navigation", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

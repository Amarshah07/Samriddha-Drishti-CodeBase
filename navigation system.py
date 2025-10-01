import cv2
import torch
import numpy as np
import pyttsx3
import time

# === Initialize Text-to-Speech === #
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)  # Normal speaking speed
last_instruction_time = 0
last_instruction = ""

def text_to_speech(text):
    """Convert text to speech while preventing repetition."""
    global last_instruction_time, last_instruction
    current_time = time.time()

    # Avoid repeating the same instruction within 3 seconds
    if text != last_instruction or (current_time - last_instruction_time > 3):
        print(f"🔊 Speaking: {text}")  # Debugging log
        tts_engine.say(text)
        tts_engine.runAndWait()
        last_instruction = text
        last_instruction_time = current_time

# === Load YOLOv5 Model === #
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# === Define Navigation-Relevant Objects === #
NAVIGATION_CLASSES = {"chair", "table", "wall", "door", "person"}

# === Open Webcam === #
cap = cv2.VideoCapture(1)

def process_frame(frame):
    """Process frame for object detection and navigation guidance"""
    results = model(frame)
    detections = results.xyxy[0].cpu().numpy()  # Updated API usage

    height, width, _ = frame.shape
    navigation_instructions = []
    obstacle_detected = False  # Flag to determine if an obstacle is present

    for *xyxy, conf, cls in detections:
        x1, y1, x2, y2 = map(int, xyxy)
        obj_name = model.names[int(cls)]

        if obj_name in NAVIGATION_CLASSES:
            obstacle_detected = True
            center_x = (x1 + x2) / 2

            # Determine object position (left, center, right)
            if center_x < width * 0.3:
                position = "left"
            elif center_x > width * 0.7:
                position = "right"
            else:
                position = "center"

            # Generate smart navigation instructions
            if obj_name == "wall":
                instruction = "Stop! Wall ahead."  
            elif obj_name == "person":
                instruction = f"Person ahead, stay {position}."
            elif obj_name == "chair" or obj_name == "table":
                instruction = f"Move slightly {position} to avoid the {obj_name}."
            elif obj_name == "door":
                instruction = f"Turn {position}, door ahead."

            if instruction:
                navigation_instructions.append(instruction)

            # Draw bounding box around detected objects
            color = (0, 255, 0) if obj_name != "wall" else (0, 0, 255)  # Red for wall, Green for others
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, f"{obj_name} ({position})", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # If no obstacles, give a "clear path" instruction
    if not obstacle_detected:
        navigation_instructions.append("Path is clear. Keep walking.")

    return frame, navigation_instructions

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    processed_frame, instructions = process_frame(frame)

    # Display frame with bounding boxes
    cv2.imshow("Navigation Assistance", processed_frame)

    # Speak only relevant instructions
    if instructions:
        text_to_speech(" ".join(instructions))

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

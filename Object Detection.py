import cv2
import torch
import pyttsx3
import time

model = torch.hub.load('ultralytics/yolov5', 'custom', path=r'C:\Users\Amar shah\Documents\Python\yolo v5\yolov5-master\yolov5s.pt')

engine = pyttsx3.init()

def speech(text):
    print(text)
    engine.say(text)
    engine.runAndWait()
#webcam
video = cv2.VideoCapture(0)

labels_last_announced = {}
min_time_between_announcements = 6
while True:
    ret, frame = video.read()
    if not ret:
        break

    results = model(frame)

    
    cv2.imshow('YOLOv5 Object Detection', results.render()[0])

    current_time = time.time()

    labels = results.names
    for *box, conf, cls in results.xyxy[0]:
        label = labels[int(cls)]
        if label not in labels_last_announced or (current_time - labels_last_announced[label]) > min_time_between_announcements:
            speech(f"I saw {label}")
            labels_last_announced[label] = current_time


    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

video.release()
cv2.destroyAllWindows()

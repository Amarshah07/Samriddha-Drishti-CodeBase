import cv2
import numpy as np
import pyttsx3
import newreading
import time
import threading

# === Initialize EasyOCR Reader (GPU enabled for speed) === #
reader = newreading.Reader(['en'], gpu=True)

# === Initialize Text-to-Speech (Non-Blocking) === #
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 120)  # Adjust speed

speech_lock = threading.Lock()  # Prevents overlapping speech

def speak(text):
    """Handles speech output in a separate thread to avoid lag."""
    def run_tts():
        with speech_lock:
            tts_engine.say(text)
            tts_engine.runAndWait()
    threading.Thread(target=run_tts, daemon=True).start()

# === Open Webcam (Optimized Settings) === #
video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

last_text = ""
min_time_between_announcements = 7  # Delay before repeating the same text

while True:
    ret, frame = video.read()
    if not ret:
        break

    # Convert frame to grayscale (improves OCR accuracy)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect text using EasyOCR
    results = reader.readtext(gray_frame)
    detected_text = " ".join([res[1] for res in results])  # Extract detected text

    # Speak only if new text is detected
    if detected_text and detected_text != last_text:
        print(f"Detected Text: {detected_text}")
        speak(detected_text)
        last_text = detected_text
        time.sleep(min_time_between_announcements)  # Pause before reading again

    # Display the webcam feed
    cv2.imshow("Reading Mode - AI Glasses", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()

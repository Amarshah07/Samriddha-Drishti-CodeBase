import bluetooth
import threading
import pyttsx3
import speech_recognition as sr
import cv2
import time
import queue

# ======================
# TTS Setup
# ======================
engine = pyttsx3.init()
speech_queue = queue.Queue()

def tts_worker():
    while True:
        text = speech_queue.get()
        if text is None:
            break
        engine.say(text)
        engine.runAndWait()
        speech_queue.task_done()

threading.Thread(target=tts_worker, daemon=True).start()

def speak(text):
    print(f"🔊 Speaking: {text}")
    speech_queue.put(text)

# ======================
# Bluetooth Blind Stick Listener
# ======================
blind_stick_addr = None
blind_stick_port = 1

def find_blind_stick():
    global blind_stick_addr
    print("🔍 Scanning for Blind Stick...")
    nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True)
    for addr, name in nearby_devices:
        if "BlindStick" in name:
            blind_stick_addr = addr
            print(f"✅ Found Blind Stick at {addr}")
            return
    print("❌ Blind Stick not found.")

def blind_stick_listener():
    if blind_stick_addr is None:
        find_blind_stick()
    if blind_stick_addr is None:
        return

    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((blind_stick_addr, blind_stick_port))
    print("📡 Connected to Blind Stick.")

    while True:
        try:
            data = sock.recv(1024).decode("utf-8").strip()
            if data:
                print(f"📡 Blind Stick Data: {data}")
                speak(f"Obstacle detected: {data}")
        except Exception as e:
            print(f"❌ Blind Stick Error: {e}")
            break

# ======================
# AI Glasses Listener
# ======================
cap = cv2.VideoCapture(0)
recognizer = sr.Recognizer()

def glasses_listener():
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        # Here you can add YOLO or Vision AI processing
        # For demo, we just display frame
        cv2.imshow("AI Glasses Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

# ======================
# Start Threads
# ======================
threading.Thread(target=blind_stick_listener, daemon=True).start()
threading.Thread(target=glasses_listener, daemon=True).start()

# ======================
# Keep Running
# ======================
print("🧠 Mobile Hub running...")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n👋 Exiting Mobile Hub.")
    cap.release()
    cv2.destroyAllWindows()
    speech_queue.put(None)

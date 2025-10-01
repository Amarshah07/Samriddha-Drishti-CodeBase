import cv2
import torch
import pyttsx3
import speech_recognition as sr
import threading
from transformers import BlipProcessor, BlipForQuestionAnswering, BlipForConditionalGeneration

# === Initialize Text-to-Speech === #
engine = pyttsx3.init()
engine.setProperty('rate', 130)

def speak_text(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

# === Initialize Speech Recognition === #
recognizer = sr.Recognizer()
mic = sr.Microphone()

def listen_command():
    """Capture voice command from the user with error handling."""
    with mic as source:
        print("\n🎤 Listening for command...")
        recognizer.adjust_for_ambient_noise(source, duration=0.3)  # Faster adaptation
        try:
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=7)
            command = recognizer.recognize_google(audio).strip().lower()  # Strip spaces and lowercase
            print(f"🔊 You said: {command}")  # Debugging log
            return command
        except sr.WaitTimeoutError:
            print("⏳ No speech detected. Try again.")
            return None  
        except sr.UnknownValueError:
            print("❌ Could not understand. Try again.")
            return None
        except sr.RequestError:
            print("❌ Speech recognition service error.")
            return None

# === Load BLIP Processor and Models === #
processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")  
scene_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")  
vqa_model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")  

# === Initialize Webcam === #
video = cv2.VideoCapture(1)  ;

if not video.isOpened():
    print("Error: Could not open webcam.")
    exit()

# === Multithreading for Faster Video Display === #
frame = None
running = True

def video_stream():
    """ Continuously capture frames for fast display. """
    global frame, running
    while running:
        ret, frame = video.read()
        if not ret:
            print("Error: Failed to capture image.")
            running = False
            break
        cv2.imshow("AI Vision Assistant - Voice Controlled", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False
            break

# Start webcam streaming in a separate thread
threading.Thread(target=video_stream, daemon=True).start()

print("\n🎤 Say 'Describe' to capture & describe the scene.")
print("🎤 Say 'Exit' anytime to stop questioning.")
print("🎤 Say 'Quit' to close the program.")

while running:
    command = listen_command()
    if command is None:
        continue  

    if "describe" in command and frame is not None:
        # === Capture Scene and Describe === #
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        inputs = processor(images=image, return_tensors="pt")

        with torch.no_grad():
            output = scene_model.generate(**inputs, max_length=50)
        description = processor.batch_decode(output, skip_special_tokens=True)[0]

        print(" Scene Description:", description)
        speak_text(description)

        # === Question-Answering Mode === #
        while True:
            speak_text("Ask a question or say Exit to stop.")
            question_command = listen_command()
            
            if question_command is not None:
                print(f"🔎 Recognized Command: {question_command}")  # Debugging log

            if question_command == "exit":  # Exact match
                print("\n🔄 Returning to normal mode. Waiting for 'Describe' command...")
                break  

            if question_command:
                question_inputs = processor(images=image, text=question_command, return_tensors="pt")
                with torch.no_grad():
                    answer_output = vqa_model.generate(**question_inputs, max_length=50)
                answer = processor.batch_decode(answer_output, skip_special_tokens=True)[0]

                print("\n🔍 AI Answer:", answer)
                speak_text(answer)

    elif "quit" in command:
        print("\n👋 Exiting program.")
        running = False  # Stop video stream
        break  

# Cleanup
video.release()
cv2.destroyAllWindows()



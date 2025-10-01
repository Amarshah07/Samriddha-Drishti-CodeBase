import cv2
import os
import tempfile
import speech_recognition as sr
import pyttsx3
from google import genai

# Initialize TTS
engine = pyttsx3.init()

def speak(text):
    print(f"🔊 Speaking: {text}")
    engine.say(text)
    engine.runAndWait()

# Gemini API Key
client = genai.Client(api_key="AIzaSyBpPYTDS-fnZOqRYukaZACSAXsxes5Ry4Y")

# Speech recognizer
recognizer = sr.Recognizer()

print("🦾 Gemini Vision Assistant Ready")
print("🗣️ Ask a question. Say 'quit' to exit.\n")

# 📌 Default instruction for Gemini to keep it simple
default_prompt_prefix = (
    "You are assisting a blind person. "
    "Please describe the answer in a very short and simple way, "
    "avoiding any technical terms or bounding boxes. Respond like: "
    "'There is a chair in front of you' or 'A switch is on your left'.\n"
)

while True:
    try:
        print("\n🎙️ Listening for question...")
        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=15, phrase_time_limit=8)
        command = recognizer.recognize_google(audio)
        print("🔊 You said:", command)

        if "quit" in command.lower():
            speak("Goodbye!")
            break

        # Capture webcam frame
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        if not ret:
            print("❌ Failed to capture image from webcam.")
            speak("Failed to capture image from webcam.")
            continue

        # Save image to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as f:
            image_path = f.name
            cv2.imwrite(image_path, frame)

        # Upload image to Gemini
        gemini_image = client.files.upload(file=image_path)

        # Combine default prompt with user's command
        full_prompt = default_prompt_prefix + command

        # Generate content from Gemini
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[gemini_image, full_prompt]
        )
        answer = response.text.strip()

        # Remove bounding box outputs or JSON if accidentally returned
        if "box" in answer.lower() or "{" in answer:
            answer = "Sorry, I couldn't understand. Please ask again clearly."

        print("🤖 Gemini:", answer)
        speak(answer)

        # Clean up
        os.remove(image_path)

    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
        #speak("Sorry, I didn't catch that.")
    except sr.RequestError as e:
        print(f"❌ Speech Recognition Error: {e}")
        #speak("There was an error with the speech recognition service.")
    except Exception as e:
        print(f"❌ Gemini Error: {e}")
        #speak("There was an error answering your question.")

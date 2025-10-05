import cv2
import os
import tempfile
import speech_recognition as sr
from gtts import gTTS
import pyglet
from google import genai

# Function to speak text using Google TTS
def speak(text, lang='hi'):
    print(f"🔊 बोल रहा हूँ: {text}")  # Print in Hindi
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save("speech.mp3")  # Save the audio to a temporary file

    # Load and play the audio using pyglet
    sound = pyglet.media.load("speech.mp3", streaming=False)
    sound.play()

    # Wait for the sound to finish before continuing
    pyglet.app.run()

# Gemini API Key
client = genai.Client(api_key="Your_API_KEY")

# Speech recognizer
recognizer = sr.Recognizer()

print("🦾 जेमिनी विज़न असिस्टेंट तैयार है")
print("🗣️ सवाल पूछें, 'quit' कहने से बंद होगा\n")

while True:
    try:
        print("\n🎙️ सवाल सुन रहा हूँ...")
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
        command = recognizer.recognize_google(audio, language="hi-IN")  # Hindi Language
        print("🔊 आपने कहा:", command)

        if "quit" in command.lower():
            speak("अलविदा!")
            break

        # Capture webcam frame
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        if not ret:
            print("❌ कैमरे से चित्र नहीं मिल पाया।")
            speak("कैमरे से चित्र नहीं मिल पाया।")
            continue

        # Save image to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as f:
            image_path = f.name
            cv2.imwrite(image_path, frame)

        # Upload image to Gemini
        gemini_image = client.files.upload(file=image_path)

        # Generate content from Gemini
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[gemini_image, command]
        )
        answer = response.text.strip()
        print("🤖 जेमिनी:", answer)
        speak(answer)

        # Clean up
        os.remove(image_path)

    except sr.UnknownValueError:
        print("❌ आवाज़ नहीं समझ पाया।")
        speak("माफ़ कीजिए, समझ नहीं पाया।")
    except sr.RequestError as e:
        print(f"❌ स्पीच रिकग्निशन में त्रुटि: {e}")
        speak("स्पीच सेवा में कोई त्रुटि है।")
    except Exception as e:
        print(f"❌ जेमिनी त्रुटि: {e}")
        speak("कोई त्रुटि हुई।")


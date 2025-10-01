import cv2
import easyocr
import pyttsx3
import time

# Initialize EasyOCR Reader (English)
reader = easyocr.Reader(['en'])

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Speech speed

# Initialize Camera
cap = cv2.VideoCapture(1)  # Use webcam

previous_text = ""
last_read_time = 0

print("Reading Mode Activated... Press 'q' to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to access camera.")
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect text using EasyOCR
    result = reader.readtext(gray, detail=0)

    # Combine detected text
    extracted_text = " ".join(result).strip()

    # Read Text only if it's new and enough time has passed
    if extracted_text and extracted_text != previous_text and time.time() - last_read_time > 4:
        print("Detected Text:", extracted_text)

        # Speak the text
        engine.say(extracted_text)
        engine.runAndWait()

        # Update last read text and time
        previous_text = extracted_text
        last_read_time = time.time()

    # Display Camera Feed (Optional, for testing)
    cv2.imshow("Reading Mode - Press 'q' to Exit", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
print("Reading Mode Exited.")

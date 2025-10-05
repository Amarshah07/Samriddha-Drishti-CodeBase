import cv2
import face_recognition
import os
import pyttsx3
import time

# === Initialize Text-to-Speech Engine (Fast) === #
def initialize_engine():
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Adjust speech speed
    return engine

def speak(engine, text):
    print(f"Speaking: {text}")  # Debugging log
    engine.say(text)
    engine.runAndWait()

# === Load Known Faces Efficiently === #
def load_known_faces(known_faces_path):
    known_encodings, known_names = [], []
    for person_name in os.listdir(known_faces_path):
        person_folder = os.path.join(known_faces_path, person_name)
        for img_name in os.listdir(person_folder):
            img_path = os.path.join(person_folder, img_name)
            image = face_recognition.load_image_file(img_path)
            encodings = face_recognition.face_encodings(image)

            if encodings:  
                known_encodings.append(encodings[0])
                known_names.append(person_name.lower())  # Store in lowercase to avoid mismatches
            else:
                print(f"⚠ Warning: No encodings found for {person_name}")
    return known_encodings, known_names

# === Recognize Faces (Optimized) === #
def recognize_face(frame, known_encodings, known_names, last_spoken, engine):
    rgb_small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)  # Speed up processing
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    detected_name = ""
    current_time = time.time()

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.6)
        if True in matches:
            detected_name = known_names[matches.index(True)]

    if detected_name != "":
        if detected_name not in last_spoken or (current_time - last_spoken[detected_name]) > 5:
            speak(engine, f"Looks Like {detected_name.capitalize()}")
            last_spoken[detected_name] = current_time

    return detected_name

# === Main Function: Run Face Recognition === #
def detect_faces(known_faces_path):
    cap = cv2.VideoCapture(1)
    known_encodings, known_names = load_known_faces(known_faces_path)  # Preload for fast execution
    engine = initialize_engine()
    last_spoken = {}

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Cannot access camera.")
            break

        detected_name = recognize_face(frame, known_encodings, known_names, last_spoken, engine)
        print(f"Detected: {detected_name}")  # Debugging log (no GUI needed)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
            break
        
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    known_faces_path = "faces"
    detect_faces(known_faces_path)

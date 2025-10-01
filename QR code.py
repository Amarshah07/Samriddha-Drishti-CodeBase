import cv2
from pyzbar.pyzbar import decode
import pyttsx3

def speak_text(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 130)
    engine.say(text)
    engine.runAndWait()

def qr_code_scanner():
    # Open a connection to the default camera (0 represents the default camera)
    cap = cv2.VideoCapture(1)

    while True:
        # Read a frame from the camera
        _, frame = cap.read()

        # Decode QR codes
        decoded_objects = decode(frame)

        # Loop through the detected QR codes
        for obj in decoded_objects:
            # Extract the QR code data
            data = obj.data.decode('utf-8')

            # Get the bounding box coordinates
            rect_points = obj.rect
            rect_x, rect_y, rect_w, rect_h = rect_points

            # Draw a rectangle around the QR code
            cv2.rectangle(frame, (rect_x, rect_y), (rect_x + rect_w, rect_y + rect_h), (0, 255, 0), 2)

            # Speak the QR code data
            speak_text("Qr code : " + data)

        # Display the video feed with QR code detection
        cv2.imshow('QR Code Scanner', frame)

        # Exit the loop when the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    qr_code_scanner()
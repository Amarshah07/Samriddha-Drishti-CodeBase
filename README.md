# Samriddha-Drishti-CodeBase


🦾 Samriddha Drishti – AI-Powered Smart Glasses

Samriddha Drishti is an assistive AI system designed to enhance mobility and situational awareness for visually impaired individuals. It combines wearable AI vision, smart blind stick sensors, voice interaction, and navigation assistance into one integrated system.

📌 Project Overview

This project implements a voice-interactive AI vision system using Google Gemini Vision AI, object detection (YOLOv5), scene description (BLIP), and real-time speech recognition. The system captures live visuals, processes them with AI, and delivers voice-based descriptions and alerts to the user.

The software also includes a GUI mode selector for managing multiple assistive modes, such as object detection, face recognition, QR scanning, navigation, and reading.

⚙️ Features

Head & Ground Obstacle Detection (via glasses camera + ultrasonic stick sensors)

Scene Description & Visual Question Answering (VQA)

Text Reading & Cash Recognition

Face Recognition & QR Code Detection

AI Voice Assistant for natural interaction

GPS-Based Navigation & SOS Alerts

Hands-Free Mobility Assistance

🛠 Technical Stack

Vision AI: Google Gemini Pro Vision, BLIP, YOLOv5-tiny

Hardware: Smart glasses (camera + mic), smart blind stick (ultrasonic sensors), ESP32/Arduino, vibration motor, Li-ion battery

Software: Python, OpenCV, CustomTkinter (GUI), pyttsx3, speech_recognition

Communication: Bluetooth Low Energy (BLE)

TTS: Android-native text-to-speech

Navigation: GPS integration

Optimization: Low-light enhancement, model compression, power management

🗂 Folder Structure
Samriddha-Drishti/
│
├── object detection.py       # YOLOv5 object detection module
├── face recognition.py       # Face recognition module
├── gemini_scene.py           # Gemini-based scene description module
├── QR code.py                # QR code scanning module
├── IN Nav.py                 # GPS-based navigation module
├── main_gui.py               # GUI mode selector
├── README.md                 # Project documentation
└── requirements.txt          # Python dependencies

🖥 How It Works

Process Flow:

Glasses Layer:

Camera → Captures live visuals

Microphone → Captures user voice commands

Smart Stick Layer:

Ultrasonic sensors → Detect ground obstacles

Vibration motor → Provide haptic feedback

Bluetooth module → Transmit data to mobile device

AI Layer (Mobile Hub):

YOLOv5-tiny, BLIP, Gemini Vision → Object detection & scene understanding

Sensor fusion → Combine stick & glasses data

GPS → Location tracking & navigation

Feedback Layer:

Audio through glasses speaker

Vibration alerts via stick

Features Layer:

Obstacle detection, scene description, VQA

Text reading & cash recognition

Face & QR recognition

AI voice assistant

Navigation & SOS alerts

🛠 Installation

Clone the repository:

git clone https://github.com/yourusername/Samriddha-Drishti.git
cd Samriddha-Drishti


Install dependencies:

pip install -r requirements.txt


Replace "YOUR_API_KEY" in gemini_scene.py with your Gemini API key.

Run the main GUI:

python main_gui.py

🎯 Usage

Launch the GUI (main_gui.py).

Toggle any assistive mode ON/OFF (ObjectFinder, Face Recognition, Drishti Vision, QR Scanner, Navigation).

Speak your command to the system.

Receive real-time voice feedback and alerts.

📚 References

WHO World Report on Vision: https://www.who.int/publications/i/item/world-report-on-vision

YOLOv5 Object Detection: https://github.com/ultralytics/yolov5

BLIP Vision-Language Model: https://github.com/salesforce/BLIP

Google Gemini Vision AI: https://cloud.google.com/vertex-ai/docs/generative/vision

Ultrasonic Navigation Systems: Borenstein et al., IEEE Trans. on Robotics, 2021

Assistive Technology for Visually Impaired: Gandhi & Ghosh, Int. J. Eng. Adv. Technol., 2022

⚡ Future Improvements

Optimize real-time performance with edge computing

Add offline scene description support

Improve low-light vision capabilities

Integrate route planning for navigation mode

Miniaturize hardware for better ergonomics

📜 License

This project is licensed under the MIT License. See the LICENSE
 file for details.

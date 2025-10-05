# Samriddha Drishti — System Architecture

## Overview
Samriddha Drishti is a hybrid assistive mobility system integrating smart glasses with AI vision and a smart blind stick with ultrasonic sensors. It provides visually impaired individuals with real-time obstacle detection, scene understanding, navigation assistance, and emergency support.

## System Components

### 1. Smart Blind Stick
- Ultrasonic Sensors: Detect ground-level obstacles (stairs, curbs, potholes).
- Infrared Sensors: Enhance obstacle detection accuracy in low light.
- Vibration Motor: Provides haptic feedback to users.
- SOS Button: Sends GPS location to a caregiver.

### 2. Smart Glasses
- Camera + Microphone: Captures real-time scene data and user voice commands.
- Vision AI Models: Gemini Pro Vision, BLIP, YOLOv8 for object detection, scene description, and VQA.
- Audio Feedback: Text-to-Speech (TTS) guides the user.
- QR & Face Recognition: Provides contextual information instantly.

### 3. Mobile Device Hub
- Bluetooth Low Energy (BLE) connectivity with stick and glasses.
- Data fusion of vision and sensor inputs.
- Real-time navigation module and hazard alerts.
- Central processing and user interaction.

## System Flow

User Interaction → Smart Glasses Capture Scene + Audio Input → Vision AI Processing
Smart Stick → Ultrasonic Sensors Capture Ground Obstacles → BLE Transfer to Hub
Mobile Hub → Fuse Data → Generate Audio Feedback & Vibration Alerts


## Features
- Real-time obstacle detection at head-level and ground-level.
- Voice-based navigation assistance.
- Scene description and VQA for situational awareness.
- Affordable and portable design.

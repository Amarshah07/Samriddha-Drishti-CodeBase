# Samriddha Drishti - Smart Blind Stick Firmware (prototype)


## (still researching on Lidar sensor)

## Overview
ESP32 firmware for the Samriddha Drishti smart blind stick. Reads HC-SR04 ultrasonic distance, analog IR down-facing sensor for drop detection, supports vibration feedback, SOS button, and publishes JSON telemetry via Bluetooth Serial.

## Features
- Front obstacle detection (HC-SR04)
- Downward drop/stair detection (IR analog)
- Haptic feedback (vibration motor)
- SOS long-press (sends "SOS" message)
- Bluetooth Classic Serial (easy Android pairing)
- Simple JSON telemetry messages for the mobile hub

## Hardware (example)
- ESP32 Dev Board
- HC-SR04 ultrasonic sensor
- Analog IR sensor or reflectance sensor
- Vibration motor + N-channel MOSFET + diode
- Push button for SOS
- Battery + power management recommended

## How to use
1. Flash `stick.ino` using Arduino IDE (select ESP32).
2. Pair phone to "Samriddha_Stick" via Bluetooth.
3. Run `mobile_hub/python_receiver.py` or Android demo to receive JSON messages.

## Notes / Next steps
- Tune thresholds (DIST_ALERT_CM, IR_DROP_THRESHOLD) per real prototype.
- Add power management (deep-sleep between readings) for longer battery life.
- Implement firmware OTA and unique device IDs for production.

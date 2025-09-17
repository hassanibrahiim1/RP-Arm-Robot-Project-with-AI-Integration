# RP-Arm-Robot-Project-with-AI-Integration
A simple project that makes a 2-servo robotic arm (pan-tilt) track colored objects using a webcam and computer vision. The AI on a PC finds the object and sends movement commands to an ESP32 microcontroller that controls the servos.

## How It Works

1.  **PC (Python):** The `ai.py` script uses your webcam to look for a specific color you choose.
2.  **AI Vision:** It finds the largest object of that color and calculates its position on the screen.
3.  **Communication:** The PC converts the object's position into servo angles (pan and tilt) and sends them to the ESP32 over USB.
4.  **ESP32 (Arduino C++):** The `code.ino` program running on the ESP32 listens for these commands and moves the two servos to the correct angles, making the camera "look at" the object.

## What You Need

*   **Hardware:**
    *   ESP32 Development Board
    *   Two SG90 Servo Motors (or similar)
*   **Software:**
    *   Arduino IDE (to upload code to the ESP32)
    *   Python 3.8+ (on your PC)
*   **Other:**
    *   A USB webcam
    *   Jumper wires and a breadboard
    *   USB cable to connect the ESP32 to your PC

## Setup Instructions

### 1. ESP32 Setup (Upload the Firmware)

1.  Connect your ESP32 to your PC via USB.
2.  Open the `code.ino` file in the Arduino IDE.
3.  Install the `ESP32Servo` library if you don't have it (Tools -> Manage Libraries -> Search for "ESP32Servo").
4.  Select your ESP32 board and the correct COM port in the Arduino IDE.
5.  Wire your servos:
    *   Servo 1 (Pan): Signal wire to GPIO **22**
    *   Servo 2 (Tilt): Signal wire to GPIO **23**
    *   Servo Power: Connect all `Vcc` (red) to ESP32 `5V` or `Vin` (if using external power).
    *   Servo Ground: Connect all `GND` (brown/black) to ESP32 `GND`.
6.  Click **Upload** to send the code to your ESP32.

### 2. PC Setup (Run the AI Script)

1.  Open a terminal on your PC.
2.  Install the required Python libraries:
    ```bash
    pip install opencv-python numpy pyserial
    ```
3.  Find the COM port number of your ESP32 (e.g., `COM7` on Windows, `/dev/ttyUSB0` on Linux). You can find this in the Arduino IDE under Tools -> Port.
4.  In the `ai.py` file, change the line `ser = serial.Serial('COM7', 115200, timeout=1)` to use your ESP32's COM port.

## How to Run It

1.  Make sure the ESP32 is connected and the code is uploaded.
2.  Run the Python script on your PC:
    ```bash
    python ai.py
    ```
3.  The script will ask for a color. Type one of the supported colors: `red`, `green`, `blue`, `yellow`, or `black`.
4.  A window will open showing your webcam feed. Hold a colored object in front of the camera.
5.  The AI will draw a box around the object it detects.
6.  Press the **'c'** key on your keyboard to confirm and send the servo angles to the ESP32. The arm will move to point at the object.
7.  Press **'q'** to quit the program.

## Troubleshooting

*   **Servos not moving?** Double-check your wiring and make sure the ESP32 is powered properly.
*   **Serial connection error?** Make sure you are using the correct COM port in the `ai.py` script and that the ESP32 is not busy (close the Arduino IDE Serial Monitor).
*   **Can't detect color?** Lighting is important! Try under different light conditions. You can also adjust the color values in the `COLOR_RANGES` dictionary in `ai.py`.

#include <ESP32Servo.h>

Servo servo1;  // Create a servo object for the first motor
Servo servo2;  // Create a servo object for the second motor

const int servo1Pin = 22; // Define the digital pin for the first servo
const int servo2Pin = 23; // Define the digital pin for the second servo

void setup() {
  Serial.begin(115200); // Initialize serial communication at 115200 baud rate
  servo1.attach(servo1Pin); // Attaches the servo on pin 16 to the servo object
  servo2.attach(servo2Pin); // Attaches the servo on pin 17 to the servo object
  Serial.println("Servo control via serial started. Send 'a' for servo 1, 'b' for servo 2 followed by the angle (0-180).");
  Serial.println("Example: a90 (moves servo 1 to 90 degrees), b180 (moves servo 2 to 180 degrees)");
}

void loop() {
  
  if (Serial.available() > 0) {
    char commandChar = Serial.read(); // Read the first character to determine the servo

    if (Serial.available() >= 3) { // Ensure there are at least 3 more characters for the angle (0-180)
      String angleString = "";
      angleString += Serial.read(); // Read the first digit
      angleString += Serial.read(); // Read the second digit
      angleString += Serial.read(); // Read the third digit

      int angle = angleString.toInt(); // Convert the string to an integer

      if (angle >= 0 && angle <= 180) {
        if (commandChar == 'a') {
          servo1.write(angle);
          Serial.print("Servo 1 moved to: ");
          Serial.println(angle);
        } else if (commandChar == 'b') {
          servo2.write(angle);
          Serial.print("Servo 2 moved to: ");
          Serial.println(angle);
        } else {
          Serial.println("Invalid servo command. Use 'a' or 'b'.");
        }
      } else {
        Serial.println("Invalid angle. Please enter a value between 0 and 180.");
      }
    } else {
      Serial.println("Incomplete command. Please send servo command followed by a 3-digit angle (e.g., a090).");
      // Clear any remaining characters in the serial buffer to avoid issues in the next loop
      while (Serial.available() > 0) {
        Serial.read();
      }
    }
  }
  delay(10); // Small delay for stability
}
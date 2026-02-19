#include <ESP32Servo.h>

Servo gateServo;

int servoPin = 18;   // Change if needed

void setup() {
  Serial.begin(115200);
  gateServo.attach(servoPin);
  gateServo.write(0);  // Gate open initially
}

void loop() {

  if (Serial.available()) {

    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "OPEN") {
      gateServo.write(0);    // Open position
    }

    if (command == "CLOSE") {
      gateServo.write(90);   // Close position
    }
  }
}

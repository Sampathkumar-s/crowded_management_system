#include <WiFi.h>
#include <ESP32Servo.h>
#include <WebServer.h>

const char* ssid = "Praveen";
const char* password = "987654321";

WebServer server(80);
Servo gateServo;

int servoPin = 13;

void handleOpen() {
  gateServo.write(0);
  server.send(200, "text/plain", "Gate Opened");
}

void handleClose() {
  gateServo.write(90);
  server.send(200, "text/plain", "Gate Closed");
}

void setup() {
  Serial.begin(115200);

  gateServo.attach(servoPin);
  gateServo.write(0);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting...");
  }

  Serial.println("Connected!");
  Serial.println(WiFi.localIP());

  server.on("/open", handleOpen);
  server.on("/close", handleClose);

  server.begin();
}

void loop() {
  server.handleClient();
}

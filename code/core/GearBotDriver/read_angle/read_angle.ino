#include <Wire.h>

#define AS5600_ADDR 0x36 // I²C address of AS5600
#define RAW_ANGLE_H 0x0C // High byte of raw angle
#define RAW_ANGLE_L 0x0D // Low byte of raw angle

void setup() {
    Serial.begin(9600);
    Wire.begin();
}

void loop() {
    int angle = readAS5600Angle();
    Serial.print("Angle: ");
    Serial.print(angle * 0.0879); // Convert to degrees
    Serial.println("°");

    delay(100); // Adjust for reading speed
}

// Function to read AS5600 raw angle
int readAS5600Angle() {
    Wire.beginTransmission(AS5600_ADDR);
    Wire.write(RAW_ANGLE_H); // Request raw angle (high byte)
    Wire.endTransmission();

    Wire.requestFrom(AS5600_ADDR, 2); // Request 2 bytes (high and low)
    if (Wire.available() == 2) {
        int high_byte = Wire.read();
        int low_byte = Wire.read();
        return (high_byte << 8) | low_byte; // Combine high and low byte
    }
    return 0; // Error case
}
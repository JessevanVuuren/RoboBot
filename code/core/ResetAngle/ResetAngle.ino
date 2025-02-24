#include <Wire.h>

#define AS5600_ADDR  0x36  // I2C address of AS5600
#define ZPOS_HIGH    0x01  // ZPOS (Zero Position) High byte
#define ZPOS_LOW     0x02  // ZPOS (Zero Position) Low byte
#define BURN_ANGLE   0x03  // Burn Angle command
#define RAW_ANGLE_H  0x0C  // Raw Angle High byte
#define RAW_ANGLE_L  0x0D  // Raw Angle Low byte

void setup() {
  Serial.begin(115200);
  Wire.begin();
  
  Serial.println("Move the encoder to the desired zero position...");
  delay(5000);  // Give time to set the position manually

  int newZero = readRawAngle();  // Get current encoder position
  newZero = newZero & 0x0FFF;  // Ensure it's a 12-bit value

  Serial.print("Setting new zero position at raw angle: ");
  Serial.println(newZero);

  // Write new zero position to ZPOS registers
  Wire.beginTransmission(AS5600_ADDR);
  Wire.write(ZPOS_HIGH);
  Wire.write((newZero >> 8) & 0x0F);  // High 4 bits
  Wire.endTransmission();

  Wire.beginTransmission(AS5600_ADDR);
  Wire.write(ZPOS_LOW);
  Wire.write(newZero & 0xFF);  // Low 8 bits
  Wire.endTransmission();

  Serial.println("Zero position temporarily set! Testing before burning...");
  delay(2000);

  int testAngle = readAdjustedAngle();
  Serial.print("Adjusted angle after setting ZPOS: ");
  Serial.println(testAngle * (360.0 / 4096.0));

  Serial.println("Burning zero position permanently...");
  delay(1000);

  // Send burn command
  Wire.beginTransmission(AS5600_ADDR);
  Wire.write(BURN_ANGLE);
  Wire.write(0x80);  // Burn permanently
  Wire.endTransmission();

  Serial.println("Burn complete! Reboot AS5600 to apply changes.");
}

void loop() {
  // Do nothing
}

int readRawAngle() {
  Wire.beginTransmission(AS5600_ADDR);
  Wire.write(RAW_ANGLE_H);
  Wire.endTransmission();
  
  Wire.requestFrom(AS5600_ADDR, 2);
  if (Wire.available() == 2) {
    int high_byte = Wire.read();
    int low_byte = Wire.read();
    return ((high_byte & 0x0F) << 8) | low_byte;  // 12-bit value
  }
  return 0;
}

int readAdjustedAngle() {
  Wire.beginTransmission(AS5600_ADDR);
  Wire.write(0x0E);  // ANGLE register
  Wire.endTransmission();
  
  Wire.requestFrom(AS5600_ADDR, 2);
  if (Wire.available() == 2) {
    int high_byte = Wire.read();
    int low_byte = Wire.read();
    return ((high_byte & 0x0F) << 8) | low_byte;  // 12-bit value
  }
  return 0;
}

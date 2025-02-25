#include "AS5600.h"      // https://github.com/RobTillaart/AS5600
#include "StepDriver.h"  // it's a meeeee, mario
#include <Wire.h>

#define SERVO_DIRE 2
#define SERVO_STEP 3

AS5600 as5600;

StepDriver motor(Stepsize::FULL_STEP, SERVO_DIRE, SERVO_STEP, 25.5);

float get_angle() {
  return as5600.readAngle() * 0.087890625;
};

void setup() {
  Serial.begin(115200);
  Wire.begin();

  as5600.begin();

  as5600.setOffset(-207.07);
  motor.set_angle(get_angle());
  
  motor.set_speed(250);
  motor.absolute_angle(90);

  while (motor.steps_to_target() != 0) {
    motor.run();
  }

  Serial.println(get_angle());
  Serial.println(motor.get_angle());
  Serial.println("");
}

void loop() {
}

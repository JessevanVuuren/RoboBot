
#include <MobaTools.h>
#include "AS5600.h"        //https://github.com/RobTillaart/AS5600
#include <Wire.h>

#define SERVO_DIRE 2
#define SERVO_STEP 3
#define STEP_SIZE 800

AS5600 as5600;

MoToStepper stepper(STEP_SIZE, STEPDIR);


void angle_begin(float offset) {
  as5600.begin();
  as5600.setOffset(offset);
}

void stepper_begin(float offset) {
  stepper.attach(SERVO_STEP, SERVO_DIRE);
  stepper.setSpeed(2500);
  stepper.setRampLen(STEP_SIZE); // Ramp length is 1/2 revolution
  stepper.rotate(1); 
}

void setup() {
  Serial.begin(115200);
  Wire.begin();

  angle_begin(-207.07);
  stepper_begin(-207.07);
}

void loop() {
  
}


#include <MobaTools.h>
#include <AccelStepper.h>  // https://github.com/waspinatorAccelStepper/tree/master //https://www.airspayce.com/mikem/arduino/AccelStepper/
#include "AS5600.h"        //https://github.com/RobTillaart/AS5600
#include <Wire.h>

#define SERVO_DIRE 2
#define SERVO_STEP 3

// AccelStepper myStepper(AccelStepper::DRIVER, SERVO_STEP, SERVO_DIRE);
AS5600 as5600;

MoToStepper stepper(800, STEPDIR);

int steps_per_revolution = 200;
int microstepping = 1;  // 1, 2, 4, 8, 16,

float desired_RPM = 300;
float max_RPM = 250;

void angle_begin(float offset) {
  as5600.begin();
  as5600.setOffset(offset);
}

void stepper_begin(float offset) {
  // float speed_steps_per_sec = (microstepping * steps_per_revolution * desired_RPM) / 60.0;
  // float max_steps_per_sec = microstepping * steps_per_revolution * max_RPM / 60;

  // Serial.println(speed_steps_per_sec);
  // Serial.println(max_steps_per_sec);

  // myStepper.setMaxSpeed(max_steps_per_sec);
  // myStepper.setAcceleration(5000);
  // myStepper.setSpeed(speed_steps_per_sec);
  // myStepper.setCurrentPosition(200);
  // myStepper.moveTo(100);
}

void setup() {
  Serial.begin(115200);
  Wire.begin();

  angle_begin(-207.07);
  // stepper_begin(-207.07);

  stepper.attach(SERVO_STEP, SERVO_DIRE);
  stepper.setSpeed(2500);
  stepper.setRampLen( 800); // Ramp length is 1/2 revolution
  stepper.rotate(1); 
}

void loop() {
  
}

#include "StepDriver.h"  // it's a meeeee, mario
#include <Wire.h>

#define SERVO_DIRE 2
#define SERVO_STEP 3

StepDriver motor(Stepsize::FULL_STEP, SERVO_DIRE, SERVO_STEP, 25.5);

int speed = 100;

void setup() {
  Serial.begin(115200);
  motor.set_speed(speed);

  Serial.println("motor start over 1 sec");
  delay(1000);
  Serial.println("motor start");

  // motor.next_angle(-50);
  motor.next_angle(-(speed/2 + 50));

  while (motor.steps_to_target() != 0) {
    motor.run();
  }

  Serial.println("motor at end");
  delay(1000);

  motor.next_angle(39);

  while (motor.steps_to_target() != 0) {
    motor.run();
  }

  Serial.println("motor done");
  Serial.println("");
  Serial.println("");

}

void loop() {
}

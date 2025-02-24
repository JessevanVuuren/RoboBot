#include "StepDriver.h"

#define SERVO_DIRE 2
#define SERVO_STEP 3

StepDriver motor(Stepsize::FOUR_STEP, SERVO_DIRE, SERVO_STEP);

void setup() {
  Serial.begin(115200);
  motor.set_speed(250);
  motor.accel_percent(10);
  motor.decel_percent(10);
  motor.set_direction(false);

  Serial.print("Sleep time: ");
  Serial.println(motor.get_interval());
}
void loop() {

  motor.run();
  if (motor.steps_to_target() == 0) {
    delay(1000);
    motor.next_angle(motor.get_angle() == 360 ? -360 : 360);
  }
}

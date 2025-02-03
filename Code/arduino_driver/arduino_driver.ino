#include <Servo.h>

#define SERVOPIN1 6
#define SERVOPIN2 5

#define BAUD 1000000

#define JOINTS 2

Servo servo1;
Servo servo2;

void setup() {
  pinMode(SERVOPIN1, OUTPUT);
  pinMode(SERVOPIN2, OUTPUT);
  
  servo1.attach(SERVOPIN1);
  servo2.attach(SERVOPIN2);
  Serial.begin(BAUD);
  Serial.setTimeout(1); 

  servo1.write(servo1.read());
  servo2.write(servo2.read());
}

int* angles_list(String dataIn) {
  static int array[JOINTS];

  int index = 0;
  int offset = 0;
  for (int i = 0; i < JOINTS; i++) {
    index = dataIn.indexOf('|', offset);
    if (index >= 0) {
      String value = dataIn.substring(offset, index);
      array[i] = value.toInt();
      offset = index + 1;
    }
  }

  return array;
}



void loop() {

  if (Serial.available()) {
    String dataIn = Serial.readStringUntil('\n');

    int* angles = angles_list(dataIn);

    Serial.print("Angle1: ");
    Serial.print(angles[0]);
    Serial.print(", Angle2: ");
    Serial.println(angles[1]);

    servo1.write(angles[0]);
    servo2.write(angles[1]);
  }
}
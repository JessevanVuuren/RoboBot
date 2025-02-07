#include <Servo.h>

#define SERVOPIN0 3
#define SERVOPIN1 6
#define SERVOPIN2 5

#define BAUD 1000000

#define ANLGES 3

Servo rotation;
Servo boom1;
Servo boom2;

void setup() {
  pinMode(SERVOPIN0, OUTPUT);
  pinMode(SERVOPIN1, OUTPUT);
  pinMode(SERVOPIN2, OUTPUT);
  
  rotation.attach(SERVOPIN0);
  boom1.attach(SERVOPIN1);
  boom2.attach(SERVOPIN2);
  
  Serial.begin(BAUD);
  Serial.setTimeout(1); 
}

int* angles_list(String dataIn) {
  static int array[ANLGES];

  int index = 0;
  int offset = 0;
  for (int i = 0; i < ANLGES; i++) {
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
    Serial.print(angles[1]);
    Serial.print(", Angle3: ");
    Serial.println(angles[2]);

    rotation.write(angles[0]);
    boom1.write(angles[1]);
    boom2.write(angles[2]);
  }
}
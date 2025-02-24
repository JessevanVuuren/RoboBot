

const int dirPin_rotate = 2;
const int stepPin_rotate = 3;

const long min_speed = 50000;
const long max_speed = 0;

void setup() {
  pinMode(dirPin_rotate, OUTPUT);
  pinMode(stepPin_rotate, OUTPUT);
  pinMode(A0, INPUT);
  digitalWrite(stepPin_rotate, HIGH);
  Serial.begin(115200);
}

void loop() {
  long pot = analogRead(A0);
  long potVal = map(pot, 0, 1024, max_speed, min_speed);

  Serial.print(pot);
  Serial.print(", ");
  Serial.println(potVal);

  digitalWrite(stepPin_rotate, HIGH);
  delayMicroseconds(2);
  digitalWrite(stepPin_rotate, LOW);
  delayMicroseconds(potVal);
}
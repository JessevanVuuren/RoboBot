#define HALL_PIN 2
#define BAUD 115200

volatile uint64_t last_pulse_time = 0;
volatile uint64_t pulse_interval = 0;
volatile bool new_pulse = false;

void setup() {
  Serial.begin(BAUD);
  pinMode(HALL_PIN, INPUT);
  attachInterrupt(digitalPinToInterrupt(HALL_PIN), rpm_hall_trigger, FALLING);
}

void loop() {
  noInterrupts();
  uint64_t delta = pulse_interval;
  new_pulse = false;
  interrupts();

  if (delta > 0) {  // Prevent division by zero
    float current_rpm = (60.0 * 1000000.0) / delta;
    Serial.print("Motor RPM: ");
    Serial.println(current_rpm);
  } else {
    Serial.println("Waiting for pulses...");
  }

  delay(100);  // Small delay to avoid excessive serial printing
}

void rpm_hall_trigger() {
  uint64_t current_time = micros();
  pulse_interval = current_time - last_pulse_time;
  last_pulse_time = current_time;
  new_pulse = true;
}

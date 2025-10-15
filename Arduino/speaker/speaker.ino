
#define SPEAKER_PIN 8
int value = 31;

void setup() {
  
}

void loop() {
  tone(SPEAKER_PIN, value, 20);
  delay(100);
  value++;
}

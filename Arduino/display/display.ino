
#include <MD_Parola.h>
#include <MD_MAX72xx.h>
#include <SPI.h>

#define HARDWARE_TYPE MD_MAX72XX::FC16_HW
#define MAX_DEVICES 4
#define CS_PIN 3

MD_Parola display = MD_Parola(HARDWARE_TYPE, CS_PIN, MAX_DEVICES);

void setup(){
  display.begin();
  Serial.begin(9600);
  display.setIntensity(0);
  display.displayClear();

  display.displayScroll("Hello, world!", PA_CENTER, PA_SCROLL_LEFT, 100);
  Serial.println("Start");
}

void loop(){
  if (display.displayAnimate()){
    display.displayReset();
    Serial.println("Reseting...");
  }
}

//import libarries
#include <MD_MAX72xx.h>
#include <MD_Parola.h>
#include <SPI.h>

//create and setup display using default SPI interface
//DIN to 11; CLK to 13; CS to 3;
#define HARDWARE_TYPE MD_MAX72XX::FC16_HW
#define MAX_DEVICES 4
#define CS_PIN 3
#define SCREEN_WIDTH 32
#define SCREEN_HEIGHT 8

MD_MAX72XX ds = MD_MAX72XX(HARDWARE_TYPE, CS_PIN, MAX_DEVICES);
//MD_Parola text_ds = MD_Parola(HARDWARE_TYPE, CS_PIN, MAX_DEVICES);

//create the initial setup for the game of life
const bool state[SCREEN_HEIGHT][SCREEN_WIDTH] = {
{1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1},
{1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1},
{1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1},
{1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1},
{1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1},
{1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1},
{1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1},
{1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1}
};

//simulation parameters
#define TICK_SPEED 200

void setup() {
  Serial.begin(9600);
  ds.begin();
  ds.control(ds.INTENSITY, 1);
  ds.clear();
}

void draw_state(){
  //draw the current state of the simulation
  for (int y = 0; y < SCREEN_HEIGHT; y++){
    for (int x = 0; x < SCREEN_WIDTH; x++){
      ds.setPoint(y, x, state[y][x]);
    }
  }
}

void loop() {
  draw_state();
  delay(TICK_SPEED);
  ds.clear();
}

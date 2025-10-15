
/*
LIFE
A rudimentary implimentation of conway's game of life on the Max7219 display
Written by Robert Jordan
*/

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
#define SCREEN_SIZE SCREEN_WIDTH*SCREEN_HEIGHT

MD_MAX72XX ds = MD_MAX72XX(HARDWARE_TYPE, CS_PIN, MAX_DEVICES);
//MD_Parola text_ds = MD_Parola(HARDWARE_TYPE, CS_PIN, MAX_DEVICES);

//create the initial setup for the game
bool state[SCREEN_HEIGHT][SCREEN_WIDTH] = {
{1,1,0,0,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,1},
{1,1,1,0,1,0,1,0,0,1,0,0,1,0,1,1,0,0,1,0,1,0,1,1,1,1,1,0,1,0,1,1},
{1,1,1,0,1,0,1,1,1,0,1,0,1,0,1,1,1,1,1,0,0,0,1,1,0,1,1,0,1,0,1,1},
{0,1,0,1,0,0,1,1,0,1,1,0,1,0,1,1,0,1,1,0,1,0,1,1,0,1,1,0,1,0,1,1},
{1,1,1,1,1,0,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,0,1,1,0,1,0,1,1},
{1,1,1,1,1,0,1,1,1,0,1,0,1,0,1,1,1,1,1,0,1,0,0,1,0,1,1,0,1,0,1,1},
{1,0,1,1,0,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,0,1,1,0,1,0,1,1},
{1,1,1,0,1,0,1,1,1,1,0,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1}
};

//simulation parameters
#define TICK_SPEED 100

void setup() {
  Serial.begin(9600);
  ds.begin();
  ds.control(ds.INTENSITY, 1);
  ds.clear();
}

void update_state(){
  //draw the current state of the simulation
  for (int y = 0; y < SCREEN_HEIGHT; y++){
    for (int x = 0; x < SCREEN_WIDTH; x++){
      //only draw live cells
      if (state[y][x]){
        ds.setPoint(y, x, 1);
      }
      //update cells
      run_rules(x, y);
    }
  }
}

bool check_cell(int x, int y){
  //first, check the cell is not out of bounds
  if ((x >= SCREEN_WIDTH || x < 0) || (y >= SCREEN_HEIGHT || y < 0)){
    return 0;
  }
  //otherwise, return it's value
  return state[y][x];
}

int count_adjacent(int x, int y){
  //count all of the surrounding cells in a clockwise pattern
  int count = 0;
  count += check_cell(x-1, y+1); //top-left
  count += check_cell(x, y+1); //top-middle
  count += check_cell(x+1, y+1); //top-right
  count += check_cell(x+1, y); //middle-right
  count += check_cell(x+1, y-1); //bottom-right
  count += check_cell(x, y-1); //bottom-middle
  count += check_cell(x-1, y-1); //bottom-left
  count += check_cell(x-1, y); //middle-left
  return count;
}

void run_rules(int x, int y){
  //get number of adjacent cells and the cell's state
  int count = count_adjacent(x, y);

  //1. Any live cell with fewer than two live neighbours dies
  if (state[y][x] && count < 2){
    state[y][x] = 0;
  }
  //2. Any live cell with two or three live neighbours lives on
  //3. Any live cell with more than three live neighbours dies
  if (state[y][x] && count > 3){
    state[y][x] = 0;
  }
  //4. Any dead cell with exactly three live neighbours becomes a live cell
  if (!state[y][x] && count == 3){
    state[y][x] = 1;
  }
}

void loop() {
  update_state();
  count_adjacent(1,6);
  delay(TICK_SPEED);
  ds.clear();
}

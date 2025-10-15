
/*
SNAKE
A small snake game using the Max7219 display
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

MD_MAX72XX ds = MD_MAX72XX(HARDWARE_TYPE, CS_PIN, MAX_DEVICES);
MD_Parola text_ds = MD_Parola(HARDWARE_TYPE, CS_PIN, MAX_DEVICES);

//setup joystick analog pins
//VRX to A0; VRY to A1; SW to A2;
#define VRX_PIN A0
#define VRY_PIN A1
#define BUTTON_PIN A2
#define HIGH_THRESHOLD 800
#define LOW_THRESHOLD 200

//setup snake
#define START_LENGTH 5
#define MAX_LENGTH 32
#define START_Y 4
#define SPEED_INCREASE 10
#define START_SPEED 350

struct snake_bit{
  char x, y;
  unsigned char dir;
};

unsigned char length;
bool has_lost;
struct snake_bit sn[MAX_LENGTH];

//setup apple
struct apple{
  char x, y;
  bool showing;
};

struct apple ap;

//animation speeds
#define LOSE_SPEED 3500
#define TITLE_SPEED 5000
#define WIN_SPEED 4000

void move_snake_bit(int i){
  //move the snake in the correct direction
  switch (sn[i].dir){
    case 0:
      sn[i].x++;
      break;
    case 1:
      sn[i].y--;
      break;
    case 2:
      sn[i].x--;
      break;
    case 3:
      sn[i].y++;
      break;
  }

  //check if the snake is of the screen
  //if so flag loose condition
  if (sn[i].x == SCREEN_WIDTH){
    has_lost = true;
  } else if (sn[i].x == -1){
    has_lost = true;
  } else if (sn[i].y == SCREEN_HEIGHT){
    has_lost = true;
  } else if (sn[i].y == -1){
    has_lost = true;
  }
}

void update_snake(){
  //move and draw the snake
  for (int i = 0; i < length; i++){
    move_snake_bit(i);

    //check if the head of the snake is coliding with any other part
    if (i != 0 && sn[0].x == sn[i].x && sn[0].y == sn[i].y){
      has_lost = true;
    }

    ds.setPoint(sn[i].y, sn[i].x, 1);
  }
  //change the direction of each bit of the snake, starting from the back
  for (int i = length; i > 0; i--){
    sn[i].dir = sn[i-1].dir;
  }
}

void check_joystick(){
  //read analouge volatage from joystick
  int xv = analogRead(VRX_PIN);
  int yv = analogRead(VRY_PIN);

  //change the direction of the head of the snake
  if (yv > HIGH_THRESHOLD && sn[0].dir != 1){
    //up
    sn[0].dir = 3;
  } else if (yv < LOW_THRESHOLD && sn[0].dir != 3){
    //down
    sn[0].dir = 1;
  } else if (xv < LOW_THRESHOLD && sn[0].dir != 2){
    //left
    sn[0].dir = 0;
  } else if (xv > HIGH_THRESHOLD && sn[0].dir != 0){
    //right
    sn[0].dir = 2;
  }

  Serial.println(xv);
  Serial.println(yv);
}

void grow_snake(){
  //work out the postion of the new bit from the direction of the end of the snake
  switch (sn[length-1].dir){
    case 0:
      sn[length].y = sn[length-1].y;
      sn[length].x = sn[length-1].x - 1;
      break;
    case 1:
      sn[length].x = sn[length-1].x;
      sn[length].y = sn[length-1].y + 1;
      break;
    case 2:
      sn[length].y = sn[length-1].y;
      sn[length].x = sn[length-1].x + 1;
      break;
    case 3:
      sn[length].x = sn[length-1].x;
      sn[length].y = sn[length-1].y - 1;
      break;
  }
  sn[length].dir = sn[length-1].dir;
  length++; 
} 

void reset_apple(){
  bool touching = true;

  //generate a new position for the apple
  //check if it is touching the snake and regenerate the position if so
  while (touching){
    ap.x = random(0, SCREEN_WIDTH);
    ap.y = random(0, SCREEN_HEIGHT);
    touching = false;

    for (int i = 0; i < length; i++){
      if (sn[i].x == ap.x && sn[i].y == ap.y){
        touching = true;
      }
    }
  }
}

void update_apple(){
  //check if the apple is touching the head of the snake
  if (ap.x == sn[0].x && ap.y == sn[0].y){
    grow_snake();
    reset_apple();
  }

  //toggle the apple on or of each frame
  if (ap.showing){
    ap.showing = false;
  } else {
    ap.showing = true;
  }

  ds.setPoint(ap.y, ap.x, ap.showing);
}

void reset_game(){
  //create snake
  for (int i = 0; i <= START_LENGTH; i++){
    sn[i].x = START_LENGTH-i;
    sn[i].y = START_Y;
    sn[i].dir = 0;
  }

  length = START_LENGTH;
  has_lost = false;

  //create apple
  ap.x = 20;
  ap.y = 4;
  ap.showing = true;

  //show the title animation util the joystick is pressed
  text_ds.setIntensity(2);
  text_ds.setInvert(true);

  while (true){
    if (text_ds.displayAnimate()){
      text_ds.displayText("SNAKE", PA_CENTER, 100, TITLE_SPEED, PA_SCROLL_DOWN, PA_SCROLL_DOWN);
    }
    if (digitalRead(BUTTON_PIN) == 0){
      break;
    }
  }
}

void lose(){
  //show the lose animation
  text_ds.setIntensity(2);
  text_ds.displayClear();
  text_ds.setInvert(false);

  //format score string
  char score_str[6];
  sprintf(score_str, "PTS:%i", length-START_LENGTH);

  for (int i = 0; i < LOSE_SPEED; i++){
    if (text_ds.displayAnimate()){
      text_ds.displayText("LOSE", PA_CENTER, 100, LOSE_SPEED, PA_SCROLL_UP, PA_SCROLL_UP);
    }
    delay(1);
  }
  for (int i = 0; i < LOSE_SPEED; i++){
    if (text_ds.displayAnimate()){
      text_ds.displayText(score_str, PA_CENTER, 100, LOSE_SPEED, PA_SCROLL_UP, PA_SCROLL_UP);
    }
    delay(1);
  }
  reset_game();
}

void win(){
  //show the win animation
  text_ds.setIntensity(2);
  text_ds.displayClear();
  text_ds.setInvert(false);

  for (int i = 0; i < WIN_SPEED; i++){
    if (text_ds.displayAnimate()){
      text_ds.displayText("WIN!", PA_CENTER, 100, LOSE_SPEED, PA_SCROLL_DOWN, PA_SCROLL_DOWN);
    }
    delay(1);
  }
  reset_game();
}

void setup() {
  Serial.begin(9600);

  ds.begin();
  ds.control(ds.INTENSITY, 5);
  text_ds.begin();
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  randomSeed(analogRead(5));
  reset_game();
}

void loop() {
  ds.clear();
  check_joystick();
  update_snake();
  update_apple();

  //speed up the game as the snake grows
  short int speed = START_SPEED - length*SPEED_INCREASE;

  delay(speed);

  if (has_lost){
    lose();
  }

  //if the length of the snake is the max, the player has won
  if (length == MAX_LENGTH){
    win();
  }
}

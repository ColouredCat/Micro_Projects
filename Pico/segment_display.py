
from machine import I2C, Pin
from time import sleep
from ht16k33segment14 import HT16K33Segment14 as Seg14x4

def draw_4digit(number, display):
    number = '{:4d}'.format(number)
    display.set_character(number[0], 0)
    display.set_character(number[1], 1)
    display.set_character(number[2], 2)
    display.set_character(number[3], 3)
    display.draw()
    
def main():
    time = 0000
    displayI2C = I2C(0, sda=Pin(12), scl=Pin(13))
    display = Seg14x4(displayI2C, is_ht16k33=True)
    
    while True:
        draw_4digit(time, display)
        sleep(1)
        time += 1
    
if __name__ == "__main__":
    main()



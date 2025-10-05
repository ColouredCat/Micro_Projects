import max7219
import input_
from machine import Pin, SPI, Timer
from time import sleep

def init():
    spi = SPI(0, baudrate=10000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
    display = max7219.Matrix8x8(spi,Pin(5), 4)
    display.fill(0)
    return display

def timer():
    display = init()

    clock = 0
    running = True

    while running:
        clock += 1
        display.fill(0)
        display.text(str(clock),0,0,1)
        display.show()
        sleep(1)
        
class Screen:
    def __init__(self):
        spi = SPI(0, baudrate=10000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
        self.display = max7219.Matrix8x8(spi, Pin(5), 4)
        self.display.fill(0)
        self.display.show()
        
    def loop(self):
        self.display.show()
        sleep(0.1)
    
class Dot:
    def __init__(self,x , y, display):
        self.dis = display.display
        self.x = x
        self.y = y
        self.dis.pixel(x, y, 1)
        
    def move(self, addX, addY):
        self.dis.pixel(self.x, self.y, 0)
        self.x += addX
        self.y += addY
        self.dis.pixel(self.x, self.y, 1)
        
screen = Screen()
sprite = Dot(0,0, screen)
running = True

while running:
        
    sprite.move(1,1)
    screen.loop()
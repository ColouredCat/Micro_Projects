# Import libries
from machine import Pin, SPI, ADC, I2C
from max7219 import Matrix8x8
from imu import MPU6050
from random import choice, randint
from time import sleep

class accel(MPU6050):
    def __init__(self):
        i2c = I2C(0, sda=Pin(20), scl=Pin(21), freq=400000)
        super().__init__(i2c)
        
    def movement(self):
        #check if the accelerometer is moving right or left
        if self.accel.y < -1:
            return -1
        if self.accel.y > 0:
            return 1
        else:
            return 0
        
class display(Matrix8x8):
    def __init__(self):
        spi = SPI(0, baudrate=96000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
        ss = Pin(5, Pin.OUT)
        super().__init__(spi, ss, 4)
        self.brightness(10)
        
class block():
    def __init__(self):
        self.x = 0
        self.y = randint(1, 6)
        self.disabled = 0
        self.shape = choice(([[1,1],[1,1]], [[1,1],[1,1]], [[1,1],[1,1]], [[1,1],[1,1]]))
        
    def draw(self, dis):
        #draw each pixel to the screen individualy
        if self.shape[0][0]:
            dis.pixel(self.x, self.y, 1)
        if self.shape[0][1]:
            dis.pixel(self.x+1, self.y, 1)
        if self.shape[1][0]:
            dis.pixel(self.x, self.y+1, 1)
        if self.shape[1][1]:
            dis.pixel(self.x+1, self.y+1, 1)
    
    def move(self, ac, touching):
        #if the block stops moving and hasn't reched the edge, it has hit another block
        if self.x+2 < 32 and self.disabled:
            return 1;
        #otherwise keep moving it
        elif self.x+2 < 32:
            self.x += 1
        else:
            #stop blocks when they reach the edge
            self.disabled = 1;
            return 1;
        
        if not touching:
            self.y -= ac.movement()
        
        #stop the block moving of the edge of the screen
        if self.y < 0:
            self.y += 1
        elif self.y > 6:
            self.y -= 1
            
        return 0;
    
class game:
    def into(self):
        self.dis.fill(1)
        self.dis.show()
        for i in range(4):
            sleep(0.5)
            self.dis.fill_rect(i*8,0,8,8,0)
            self.dis.show()
            
    def outro(self):
        for i in range(4):
            sleep(0.5)
            self.dis.fill_rect(24-i*8,0,8,8,1)
            self.dis.show()
        
        sleep(1)
        self.dis.fill(0)
        self.dis.text(str(self.score)+'P', 0, 0)
        self.dis.show()
        
    def check_rows(self):
        #check for rows of blocks
        rowx = 100
        for a in range(len(self.blocks)):
            rows = 0
            for b in self.blocks[a:len(self.blocks)]:
                #look for 4 blocks on the same x 
                if b.x == self.blocks[a].x:
                    rows += 1
                if rows == 4:
                    rowx = self.blocks[a].x
                    rows = 0
            
        #check if a row has been found
        if rowx != 100:
            #increase speed and score
            self.score += 8
            self.speed -= self.speed/14
            #delete blocks on the found row and move other ones
            for i in range(len(self.blocks)):
                if self.blocks[i].x == rowx:
                    self.blocks[i].x = 100
                if self.blocks[i].x < rowx:
                    self.blocks[i].x += 2
            
    def __init__(self):
        #setup all the pysical components
        self.ac = accel()
        self.dis = display()
        
        self.into()
        
        self.blocks = []
        self.blocks.append(block())
        
        self.speed = 0.15
        self.score = 0
        
        #loop while there is space to place blocks
        while True:
            self.dis.fill(0)
            
            #draw all blocks to the screen
            for blk in self.blocks:
                blk.draw(self.dis)
            
            self.dis.show()
            
            #loop through all blocks and check for colision with the one that's falling
            a = self.blocks[-1]
            touching = 0
            
            for b in self.blocks[0:len(self.blocks)-1]:
                if a.y+1 >= b.y and a.y-1 <= b.y and a.x+2 == b.x:
                    self.blocks[-1].disabled = 1
                #check if blocks are touching horizontaly and stop them from moving if so
                if a.x+1 >= b.x and a.x-1 <= b.x and (a.y+2 == b.y or a.y-2 == b.y):
                    touching = 1
                    
            #check if the player has died
            if self.blocks[-1].disabled and self.blocks[-1].x == 0:
                break
            
            #move the current block at the end of the list and check if a new one needs adding
            if self.blocks[-1].move(self.ac, touching):
                #add block and increase score
                self.blocks.append(block())
                self.score += 1
                
            self.check_rows()
                    
            sleep(self.speed)
            
        self.outro()
        
if __name__ == "__main__":
    while True:
        game()
        sleep(10)


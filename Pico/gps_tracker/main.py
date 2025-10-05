
#import libraries
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from gps import GPS_Module
from OSGridConverter import ll_to_os
from time import sleep

#setup display and gps
i2c = I2C(scl=Pin(21), sda=Pin(20))
dis = SSD1306_I2C(128, 64, i2c)
GPS = GPS_Module(0, 0, 1)

while True:
    #check if a fix is found
    if GPS.get_fix():
        dis.fill(0)
        dis.text(GPS.str_time(), 0, 0, 1)
        
        #get and format os grid reference from lat long
        g = ll_to_os(GPS.lat, GPS.long)
        str_g = "{} {}".format(str(round(g[0])), str(round(g[1])))
        dis.text(str_g, 0, 16, 1)
        
        dis.text(str(GPS.sat) + " sat tracked", 0, 32, 1)
    else:
        #show if no fix is found
        dis.fill(0)
        dis.text("No fix found", 0, 0, 1)
        
    dis.show()
    sleep(1)



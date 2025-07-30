
# Import libries
from machine import Pin, SPI, ADC
import max7219
import time

def get_tmp(sensor):
    adc = sensor.read_u16()

    #Convert ADC to voltage and temperature
    voltage = adc * (3.3 / 65535.0)
    tmp = 27 - (voltage - 0.706) / 0.001721
    
    #Return to 1 d.p as str
    return str(round(tmp,1))

def main():
    #Setup display
    spi = SPI(0, baudrate=96000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
    ss = Pin(5, Pin.OUT)
    display = max7219.Matrix8x8(spi, ss, 4)
    display.brightness(10)
    
    #Setup temperature sensor
    sensor = ADC(4)
    
    while True:
        #Put temperature on screen
        tmp = get_tmp(sensor)
        display.fill(0)
        display.text(tmp,0,0,1)
        display.show()
        time.sleep(0.5)
    
if __name__ == "__main__":
    main()

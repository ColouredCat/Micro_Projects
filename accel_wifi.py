
import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
from imu import MPU6050
from machine import reset, Pin, I2C
from math import sqrt

# network details
ssid = 'MARS_WiFi'
password = 'BlakieTomasRoosa767'

def open_network():
    # make connection to Wifi
    wlan = network.WLAN(network.AP_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    print('Waiting for connection...')
    
    # wait until connected
    while wlan.isconnected() == False:
        sleep(1)
    
    ip = wlan.ifconfig()[0]
    print(f"IP Address: {ip}")
    return ip

def open_socket(ip):
    send_address = ("192.168.1.132", 4020)
    sock = socket.socket()
    
    # set up accelerometer
    i2c = I2C(1, sda=Pin(26), scl=Pin(27), freq=400000)
    imu = MPU6050(i2c)
    
    try:
        sock.connect(send_address)
    except OSError:
        # reset machine if connection fails
        print("Could not connetect. Trying again...")
        return True
        
    #print(imu.accel_range())

    
    while True:
        try:
            # attempt sending data
            accel = imu.accel.xyz
            a = sqrt(accel[0]**2 + accel[1]**2 + accel[2]**2)
            sock.send(f"Acelleration is: {accel}\n".encode())
        except OSError:
            # reset on fail
            print("Lost Connection")
            return True
            
        sleep(0.5)
        
    sock.close()
    return False
    
def main():
    pico_led.on()
    ip = open_network()
    while open_socket(ip):
        pass

main()
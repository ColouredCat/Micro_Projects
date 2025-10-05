


import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine

ssid = 'MARS_WiFi'
password = 'BlakieTomasRoosa767'

def open_network():
    # make connection to Wifi
    wlan = network.WLAN(network.STA_IF)
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
    snd_address = ("192.168.1.132", 4020)
    sock = socket.socket()
    
    # attempt to connect
    try:
        sock.connect(snd_address)
    except OSError:
        # reset machine if connection fails
        print("Could not connetect. Trying again...")
        return True
        
    
    while True:
        try:
            # attempt sending data
            temp = pico_temp_sensor.temp
            sock.send(f"Temperature is: {temp}\n".encode())
        except OSError:
            # reset on fail
            print("Lost Connection")
            return True
            
        sleep(1)
        
    sock.close()
    return False
    
def main():
    pico_led.on()
    ip = open_network()
    while open_socket(ip):
        pass

    print("End: resetting")
    machine.reset()
main()
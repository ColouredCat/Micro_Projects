

from machine import Pin, UART
import time

class GPS_Module:
    
    def __init__(self, interface, txp, rxp):
        self.serial = UART(interface, baudrate=9600, tx=Pin(txp), rx=Pin(rxp))
        
        test = self.serial.readline()
        if test == b'\xff':
            print('GPS failed to initialise!')
            
    def to_degrees(self, raw_lat, raw_long):
        lat = int(raw_lat[0]+raw_lat[1])
        lat += float(raw_lat[2:-1])/60
        
        long = int(raw_long[0:2])
        long += float(raw_long[3:-1])/60
        return lat, long
        
    def get_fix(self):
        lines = self.serial.read()
        #ignore data if timeout
        if lines != None:
            #convert to ascii
            try:
                lines = lines.decode('utf-8')
            except UnicodeError:
                #if decoding fails, no fix data 
                return False
            
            lines = lines.replace('\n', ',')
            lines = lines.split(',')
            #look for $GPGGA sentance
            if '$GPGGA' in lines:
                #find position 
                idx = lines.index('$GPGGA')
                self.time = lines[idx+1]
                
                #if latitude is blank, there is no fix
                if lines[idx+2] == '':
                    return False
                
                #convert lat and long to decimal degrees
                raw_lat = str(lines[idx+2])
                raw_long = str(lines[idx+4])
                self.lat, self.long = self.to_degrees(raw_lat, raw_long)
                if lines[idx+3] == 'S':
                    self.lat = -self.lat
                if lines[idx+5] == 'W':
                    self.long = -self.long
                
                self.sat = lines[idx+7]
                self.alt = lines[idx+9]
                return True
        return False
        
def main():
    #start GPS module
    GPS = GPS_Module(0, 16, 17)
    log = open('gps_log.csv', 'a')
    while True:
        try:
            if GPS.get_fix():
                msg = "{},{},{},{},{}".format(GPS.time, str(GPS.lat), str(GPS.long), GPS.sat, GPS.alt)
                print(msg)
                log.write(msg+'\n')
                #save changes so data is kept if power is lost
                log.flush()
            else:
                print("Waiting for GPS signal...")
            time.sleep(10)
        #close the loop properly when stoped
        except KeyboardInterrupt:
            break
    log.close()

if __name__ == "__main__":
    main()

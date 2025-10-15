from machine import Pin, UART
import time

class GPS_Module:
    
    def __init__(self, interface, txp, rxp):
        #setup UART interface and check there are no errors
        self.serial = UART(interface, baudrate=9600, tx=Pin(txp), rx=Pin(rxp))
        
        test = self.serial.readline()
        if test == b'\xff':
            print('GPS failed to initialise!')
            
    def to_degrees(self, raw_lat, raw_long):
        # First 2 digits is degrees; next 2 are minutes
        lat = float(raw_lat[0:2])
        lat += float(raw_lat[2:len(raw_lat)])/60
        
        # First 3 digits is degrees; next 2 are minutes
        long = float(raw_long[0:3])
        long += float(raw_long[3:len(raw_long)])/60
        return lat, long
    
    def str_time(self):
        # Nicely format the time as a string
        return "{}:{}:{} UTC".format(self.time[0:2], self.time[2:4], self.time[4:6])
        
    def get_fix(self):
        lines = self.serial.read()
        print(lines)

        #ignore data if timeout
        if lines == None:
            return False
        
        #convert to ascii
        try:
            lines = lines.decode('utf-8')
        except UnicodeError:
            #if decoding fails, no fix data 
            return False
        
        lines = lines.replace('\n', ',')
        lines = lines.split(',')

        #look for $GPGGA sentance
        if '$GPGGA' not in lines:
            return False
        
        #find position 
        idx = lines.index('$GPGGA')
        self.time = lines[idx+1]
        
        #if latitude is blank, there is no fix
        if lines[idx+2] == '' or lines[idx+2][-1] == 'V':
            return False
        
        #convert lat and long to decimal degrees
        self.lat, self.long = self.to_degrees(lines[idx+2], lines[idx+4])
        if lines[idx+3] == 'S':
            self.lat = -self.lat
        if lines[idx+5] == 'W':
            self.long = -self.long
        
        self.sat = lines[idx+7]
        self.alt = lines[idx+9]
        return True
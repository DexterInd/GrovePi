
import grovepi
import serial, time, sys
import re

en_debug = False

def debug(in_str):
    if en_debug:
        print(in_str)

patterns=["$GPGGA",
    "/[0-9]{6}\.[0-9]{2}/", # timestamp hhmmss.ss
    "/[0-9]{4}.[0-9]{2,/}", # latitude of position
    "/[NS]",  # North or South
    "/[0-9]{4}.[0-9]{2}", # longitude of position
    "/[EW]",  # East or West
    "/[012]", # GPS Quality Indicator
    "/[0-9]+", # Number of satellites
    "/./", # horizontal dilution of precision x.x
    "/[0-9]+\.[0-9]*/" # altitude x.x
    ]

class GROVEGPS():
    def __init__(self, port='/dev/ttyAMA0', baud=9600, timeout=0):
        self.ser = serial.Serial(port, baud, timeout=timeout)
        self.ser.flush()
        self.raw_line = ""
        self.gga = []
        self.validation =[] # contains compiled regex

        # compile regex once to use later
        for i in range(len(patterns)-1):
            self.validation.append(re.compile(patterns[i]))

        self.clean_data()
        # self.get_date()  # attempt to gete date from GPS. 

    def clean_data(self):
        '''
        clean_data: 
        ensures that all relevant GPS data is set to either empty string
        or -1.0, or -1, depending on appropriate type
        This occurs right after initialisation or
        after 50 attemps to reach GPS
        '''
        self.timestamp = ""
        self.lat = -1.0    # degrees minutes and decimals of minute
        self.NS = ""
        self.lon = -1.0
        self.EW = ""
        self.quality = -1
        self.satellites = -1
        self.altitude = -1.0

        self.latitude = -1.0  #degrees and decimals
        self.longitude = -1.0
        self.fancylat = ""  #
        
    # def get_date(self):
    #     '''
    #     attempt to get date from GPS data. So far no luck. GPS does
    #     not seem to send date sentence at all
    #     function is unfinished
    #     '''
    #     valid = False
    #     for i in range(50):
    #         time.sleep(0.5)
    #         self.raw_line = self.ser.readline().strip()
    #         if self.raw_line[:6] == "GPZDA":  # found date line!
    #             print (self.raw_line)
            

    def read(self):
        '''
        Attempts 50 times at most to get valid data from GPS
        Returns as soon as valid data is found
        If valid data is not found, then clean up data in GPS instance
        '''
        valid = False
        for _ in range(50):
            time.sleep(0.5)
            self.raw_line = self.ser.readline()
            try:
                self.line = self.raw_line.decode('utf-8')
                self.line = self.line.strip()   
            except:
                self.line = ""
            debug(self.line)
            if self.validate(self.line):
                valid = True
                break

        if valid:
            return self.gga
        else:
            self.clean_data()
            return []

    def validate(self, in_line):
        '''
        Runs regex validation on a GPGAA sentence. 
        Returns False if the sentence is mangled
        Return True if everything is all right and sets internal
        class members.
        '''
        if in_line == "":
            return False
        if in_line[:6] != "$GPGGA":
            return False

        self.gga = in_line.split(",")
        debug (self.gga)

        #Sometimes multiple GPS data packets come into the stream. Take the data only after the last '$GPGGA' is seen
        try:
            ind=self.gga.index('$GPGGA', 5, len(self.gga))	
            self.gga=self.gga[ind:]
        except ValueError:
            pass

        if len(self.gga) != 15:
            debug ("Failed: wrong number of parameters ")
            debug (self.gga)
            return False
        
        for i in range(len(self.validation)-1):	
            if len(self.gga[i]) == 0:
                debug ("Failed: empty string %d"%i)
                return False
            test = self.validation[i].match(self.gga[i])
            if test == False:
                debug ("Failed: wrong format on parameter %d"%i)
                return False
            else:
                debug("Passed %d"%i)

        try:
            self.timestamp = self.gga[1]
            self.lat = float(self.gga[2])
            self.NS = self.gga[3]
            self.lon = float(self.gga[4])
            self.EW = self.gga[5]
            self.quality = int(self.gga[6])
            self.satellites = int(self.gga[7])
            self.altitude = float(self.gga[9])

            self.latitude = self.lat // 100 + self.lat % 100 / 60
            if self.NS == "S":
                self.latitude = - self.latitude
            self.longitude = self.lon // 100 + self.lon % 100 / 60
            if self.EW == "W":
                self.longitude = -self.longitude
        except ValueError:
            debug( "FAILED: invalid value")

        return True


if __name__ =="__main__":
    gps = GROVEGPS()
    while True:
        time.sleep(1)
        in_data = gps.read()
        if in_data != []:
            print (in_data)

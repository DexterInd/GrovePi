#!/usr/bin/python
###############################################################################################################                                                               
# This library is for using the GrovePi with Scratch
# http://www.dexterindustries.com/GrovePi/                                                                
# History
# ------------------------------------------------
# Author	Date           	Comments
# Karan		29 June 15     	Initial Authoring                                                        
# John		22 Feb 16   	Adding GrovePi Barometer
# Nicole	Nov 16			Added Folder support for take_picture 
# Nicole	Nov 16			Added eSpeak Support
# Nicole	18 Nov 16		Adding PivotPi support
# SimonW    22 Mar 18       Bug fix in error handling line 383
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2016  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
'''       
# 
# Based on the BrickPi Scratch Library written by Jaikrishna
#
# The Python program acts as the Bridge between Scratch & GrovePi and must be running for the Scratch program to run.
##############################################################################################################
'''
import scratch,sys,threading,math
import grovepi
import time
import os # to handle folder paths

try:
    sys.path.insert(0, '/home/pi/Dexter/PivotPi/Software/Scratch/')
    import PivotPiScratch
    pivotpi_available=True
except:
    pivotpi_available=False

# Folders where pictures get saved
defaultCameraFolder="/home/pi/Desktop/"
cameraFolder = defaultCameraFolder


# Pi user ID Number - used for setting permissions
pi_user=1000
pi_group=1000

# used is GrovePi is actually connected - allows for testing without a GrovePi
en_grovepi=1
# print debugging statements
en_debug=1

try:
    s = scratch.Scratch()
    if s.connected:
        print "GrovePi Scratch: Connected to Scratch successfully"
    #else:
    #sys.exit(0)
except scratch.ScratchError:
    print "GrovePi Scratch: Scratch is either not opened or remote sensor connections aren't enabled"
    #sys.exit(0)

class myThread (threading.Thread):     
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        while running:
            time.sleep(.2)              # sleep for 200 ms

thread1 = myThread(1, "Thread-1", 1)        #Setup and start the thread
thread1.setDaemon(True)

analog_sensors=['analogRead','rotary','sound','light','moisture']
digitalInp=['button']
digitalOp=['led','relay']
pwm=['LEDPower','buzzer','analogWrite']

def match_sensors(msg,lst):
    for i,e in enumerate(lst):
        if msg[:len(e)].lower()==e.lower():
            return i
    return -1
    
try:
    s.broadcast('READY')
except NameError:
    print "GrovePi Scratch: Unable to Broadcast"


while True:
    try:
        m = s.receive()

        while m==None or m[0] == 'sensor-update':
            m = s.receive()

        originalmsg = m[1]

        # change input to all lowercase. 
        # Users can enter any which way they want
        msg = originalmsg.lower()
        if en_debug:
            print "Rx:",originalmsg

        if msg == 'SETUP'.lower() :
            print "Setting up sensors done"
        elif msg == 'START'.lower() :
            running = True
            if thread1.is_alive() == False:
                thread1.start()
            print "Service Started"
        
        # ANALOG SENSORS
        elif match_sensors(msg,analog_sensors) >=0:
            if en_grovepi:
                s_no=match_sensors(msg,analog_sensors)
                sens=analog_sensors[s_no]
                port=int(msg[len(sens):])
                a_read=grovepi.analogRead(port)
                s.sensorupdate({sens:a_read})
                
            if en_debug:
                print msg
                print sens +'op:'+ str(a_read)
        
        elif msg[:8].lower()=="setInput".lower():
            if en_grovepi:
                port=int(msg[8:])
                grovepi.pinMode(port,"INPUT")
            if en_debug:
                print msg   
                
        elif msg[:9].lower()=="setOutput".lower():
            if en_grovepi:
                port=int(msg[9:])
                grovepi.pinMode(port,"OUTPUT")
            if en_debug:
                print msg
                
        elif msg[:11].lower()=="digitalRead".lower():
            if en_grovepi:
                port=int(msg[11:])
                grovepi.pinMode(port,"INPUT")
                d_read=grovepi.digitalRead(port)
                s.sensorupdate({'digitalRead':d_read})
            if en_debug:
                print msg
                print "Digital Reading: " + str(d_read)
        
        elif match_sensors(msg,digitalInp) >=0:
            if en_grovepi:
                s_no=match_sensors(msg,digitalInp)
                sens=digitalInp[s_no]
                port=int(msg[len(sens):])
                sens += str(port)
                grovepi.pinMode(port,"INPUT")
                d_read=grovepi.digitalRead(port)
                s.sensorupdate({sens:d_read})
            if en_debug:
                print msg,
                print sens +' output:'+ str(d_read)
                
        elif msg[:16].lower()=="digitalWriteHigh".lower():
            if en_grovepi:
                port=int(msg[16:])
                grovepi.pinMode(port,"OUTPUT")
                grovepi.digitalWrite(port,1)
            if en_debug:
                print msg
                
        elif msg[:15].lower()=="digitalWriteLow".lower():
            if en_grovepi:
                port=int(msg[15:])
                grovepi.pinMode(port,"OUTPUT")
                grovepi.digitalWrite(port,0)
            if en_debug:
                print msg

        elif match_sensors(msg,pwm) >=0:
            if en_grovepi:
                s_no=match_sensors(msg,pwm)
                sens=pwm[s_no]
                l=len(sens)
                port=int(msg[l:l+1])
                power=int(msg[l+1:])
                grovepi.pinMode(port,"OUTPUT")
                grovepi.analogWrite(port,power)
            if en_debug:
                print msg
        
        elif match_sensors(msg,digitalOp) >=0:
            if en_grovepi:
                s_no=match_sensors(msg,digitalOp)
                sens=digitalOp[s_no]
                l=len(sens)
                port=int(msg[l:l+1])
                state=msg[l+1:]
                grovepi.pinMode(port,"OUTPUT")
                if state=='on':
                    grovepi.digitalWrite(port,1)
                else:
                    grovepi.digitalWrite(port,0)
            if en_debug:
                print msg
        
        elif msg[:4].lower()=="temp".lower():
            if en_grovepi:
                port=int(msg[4:])
                [temp,humidity] = grovepi.dht(port,0)
                s.sensorupdate({'temp':temp})
            if en_debug:
                print msg
                print "temp: ",temp
        
        elif msg[:8].lower()=="humidity".lower():
            if en_grovepi:
                port=int(msg[8:])
                [temp,humidity] = grovepi.dht(port,0)
                s.sensorupdate({'humidity':humidity})
            if en_debug:
                print msg
                print "humidity:",humidity
        
        elif msg[:8].lower()=="distance".lower():
            if en_grovepi:
                port=int(msg[8:])
                dist=grovepi.ultrasonicRead(port)
                s.sensorupdate({'distance':dist})
            if en_debug:
                print msg
                print "distance=",dist
        
        elif msg[:3].lower()=="lcd".lower():
            if en_grovepi:
                if en_debug:
                    print msg[:3], msg[3:6], originalmsg[6:]

                sys.path.insert(0, '/home/pi/Dexter/GrovePi/Software/Python/grove_rgb_lcd')
                import grove_rgb_lcd 
                if msg[3:6].lower() == "col".lower(): #lower() added just for consistency. Not really needed
                    rgb = []
                    for i in range(0,6,2): 
                        rgb.append(int(msg[6:][i:i+2],16))  # convert from one hex string to three ints
                    if en_debug:
                        print "colours are:",rgb[0],rgb[1],rgb[2]
                    grove_rgb_lcd.setRGB(rgb[0],rgb[1],rgb[2])
                elif msg[3:6].lower() == "txt".lower():
                    txt = originalmsg[6:]
                    grove_rgb_lcd.setText_norefresh(txt)
                else:
                    pass
            if en_debug:
                print msg
            
        # elif msg[:10].lower()=="setOutput".lower():
        #   if en_grovepi:
        #       port=int(msg[10:])
        #       a_read=grovepi.analogRead(port)
        #       s.sensorupdate({'analogRead':a_read})
        #   if en_debug:
        #       print msg
        #       print "Analog Reading: " + str(a_read)   
        elif msg.lower()=="READ_IR".lower() or msg.lower()=="IR".lower():
            print "READ_IR!" 
            if en_ir_sensor==0:
                import lirc
                sockid = lirc.init("keyes", blocking = False)
                en_ir_sensor=1
            try:
                read_ir= lirc.nextcode()  # press 1 
                if len(read_ir) !=0:
                    print read_ir[0]
            except:
                if en_debug:
                    e = sys.exc_info()[1]
                    print "Error reading IR sensor: " + str(read_ir)
            if en_debug:
                print "IR Recv Reading: " + str(read_ir)
            if en_gpg:
                if len(read_ir) !=0:
                    s.sensorupdate({'read_ir':read_ir[0]})
                else:
                    s.sensorupdate({'read_ir':""})
        # CREATE FOLDER TO SAVE PHOTOS IN

        elif msg[:6].lower()=="FOLDER".lower():
            print "Camera folder"
            try:
                cameraFolder=defaultCameraFolder+str(msg[6:])
                if not os.path.exists(cameraFolder):
                    os.makedirs(cameraFolder)
                    os.chown(cameraFolder,pi_user,pi_group)
                    s.sensorupdate({"folder":"created"})
                else:
                    s.sensorupdate({"folder":"set"})
            except:
                print "error with folder name"

        elif msg.lower()=="TAKE_PICTURE".lower():
            print "TAKE_PICTURE!" 
            try:
                from subprocess import call
                import datetime
                newimage = "{}/img_{}.jpg".format(cameraFolder,str(datetime.datetime.now()).replace(" ","_",10).replace(":","_",10))
                photo_cmd="raspistill -o {} -w 640 -h 480 -t 1".format(newimage)
                print photo_cmd
                call ([photo_cmd], shell=True)
                os.chown(newimage,pi_user,pi_group)
                print "Picture Taken"
            except:
                if en_debug:
                    e = sys.exc_info()[1]
                    print "Error taking picture",e
                s.sensorupdate({'camera':"Error"})
            s.sensorupdate({'camera':"Picture Taken"})

        # Barometer code, pressure
        elif msg[:9].lower()=="pressure".lower():
            if en_grovepi:
                # We import here to prevent errors thrown.  If the import fails, you just get an error message instead of the communicator crashing.
                # If user is using multiple sensors and using their own image which does not have the pythonpath set correctly then 
                #    they'll just not get the output for 1 sensor, and the others will still keep working
                from grove_i2c_barometic_sensor_BMP180 import BMP085 # Barometric pressure sensor.
                bmp = BMP085(0x77, 1)           #Initialize the pressure sensor (barometer)
                press = bmp.readPressure()/100.0
                s.sensorupdate({'pressure':press})
                if en_debug:
                    print "Pressure: " + str(press)
            if en_debug:        # If Debug is enabled, print the value of msg.
                print msg

        elif (msg[:5].lower()=="SPEAK".lower()):
            try:
                if en_grovepi:
                    from subprocess import call
                    cmd_beg = "espeak -ven+f1 "
                    in_text = msg[len("SPEAK"):]
                    cmd_end = " 2>/dev/null"

                    call([cmd_beg+"\""+in_text+"\""+cmd_end], shell=True)
                if en_debug:
                    print(msg)
            except:
                print("Issue with espeak")

        # PIVOTPI
        elif pivotpi_available==True and PivotPiScratch.isPivotPiMsg(msg):
            pivotsensors = PivotPiScratch.handlePivotPi(msg)
            # print "Back from PivotPi",pivotsensors
            s.sensorupdate(pivotsensors)

        else:
            if en_debug:
                print "Ignoring: ",msg


                    
    except KeyboardInterrupt:
        running= False
        print "GrovePi Scratch: Disconnected from Scratch"
        break
    except (scratch.ScratchConnectionError,NameError) as e: #bug fix simonw 22Mar18
        while True:
            #thread1.join(0)
            print "GrovePi Scratch: Scratch connection error, Retrying"
            # print e
            time.sleep(5)
            try:
                s = scratch.Scratch()
                s.broadcast('READY')
                print "GrovePi Scratch: Connected to Scratch successfully"
                break;
            except scratch.ScratchError:
                print "GrovePi Scratch: Scratch is either not opened or remote sensor connections aren't enabled\n..............................\n"
    except:
        e = sys.exc_info()[0]
        print "GrovePi Scratch: Error %s" % e
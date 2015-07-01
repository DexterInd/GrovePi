#!/usr/bin/python
###############################################################################################################                                                               
# This library is for using the GrovePi with Scratch
# http://www.dexterindustries.com/GrovePi/                                                                
# History
# ------------------------------------------------
# Author     Date      		Comments
# Karan      29 June 15  	Initial Authoring                                                            
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)           
# 
# Based on the BrickPi Scratch Library written by Jaikrishna
#
# The Python program acts as the Bridge between Scratch & GrovePi and must be running for the Scratch program to run.
##############################################################################################################

import scratch,sys,threading,math
import grovepi
import time

en_grovepi=1
en_debug=1

try:
    s = scratch.Scratch()
    if s.connected:
        print "Connected to Scratch successfully"
	#else:
    #sys.exit(0)
except scratch.ScratchError:
    print "Scratch is either not opened or remote sensor connections aren't enabled"
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

analog_sensors=['analogRead','rotary','sound','light']
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
	print "Unable to Broadcast"
while True:
    try:
		m = s.receive()

		while m[0] == 'sensor-update' :
			m = s.receive()

		msg = m[1]
		print msg
		if msg == 'SETUP' :
			print "Setting up sensors done"
		elif msg == 'START' :
			running = True
			if thread1.is_alive() == False:
				thread1.start()
			print "Service Started"
		
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
				grovepi.pinMode(port,"INPUT")
				d_read=grovepi.digitalRead(port)
				s.sensorupdate({sens:d_read})
			if en_debug:
				print msg
				print sens +'op:'+ str(d_read)
				
		elif msg[:16].lower()=="digitalWriteHigh".lower():
			if en_grovepi:
				port=int(msg[16:])
				grovepi.digitalWrite(port,1)
			if en_debug:
				print msg
				
		elif msg[:15].lower()=="digitalWriteLow".lower():
			if en_grovepi:
				port=int(msg[15:])
				grovepi.digitalWrite(port,0)
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
				import grove_rgb_lcd 
				grove_rgb_lcd.setRGB(0,128,0)
				grove_rgb_lcd.setText(msg[3:])
			if en_debug:
				print msg
			
		elif msg[:10].lower()=="setOutput".lower():
			if en_grovepi:
				port=int(msg[10:])
				a_read=grovepi.analogRead(port)
				s.sensorupdate({'analogRead':a_read})
			if en_debug:
				print msg
				print "Analog Reading: " + str(a_read)		
				
		else:
			if en_debug:
				print "m",msg
				print "Wrong Command"
					
    except KeyboardInterrupt:
        running= False
        print "Disconnected from Scratch"
        break
    except (scratch.scratch.ScratchConnectionError,NameError) as e:
		while True:
			#thread1.join(0)
			print "Scratch connection error, Retrying"
			time.sleep(5)
			try:
				s = scratch.Scratch()
				s.broadcast('READY')
				print "Connected to Scratch successfully"
				break;
			except scratch.ScratchError:
				print "Scratch is either not opened or remote sensor connections aren't enabled\n..............................\n"
    except:
		print "Error"	

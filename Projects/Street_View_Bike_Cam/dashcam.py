# -*- coding: utf-8 -*-

import grovepi
import grove_rgb_lcd as lcd
import dextergps
import time
import picamera
import atexit,sys
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime,timedelta

###############################################
@atexit.register
def cleanup():
	print ("Cleanup")
	try:
		grovepi.digitalWrite(led,0)
		lcd.setRGB(0,0,0)
		lcd.setText("")
		fobj.close()
	except:
		pass
###############################################

###############################################
# LED on D7 # only for big brother GrovePi  
# DHT on D3
# LCD on I2C
# GPS on RPISER
###############################################
# Variables - adapt as needed
###############################################
photo_location = "/media/KINGSTON/"
logfile=photo_location+"trip.csv"
led = 7
dht_sensor_port = 3
dht_sensor_type = 0
temp = 0
hum = 0
use_lcd = True  # if lcd display is used for feedback
overlay_txt_ypos = 440
#degree_sign= u'\N{DEGREE SIGN}'
###################################


def display(in_str,bgcol=(255,255,255),in_lcd=use_lcd):
	print(in_str)
	try:
		if in_lcd:
			lcd.setRGB(bgcol[0],bgcol[1],bgcol[2])
			lcd.setText(in_str)
	except KeyboardInterrupt:
		sys.exit()
	except:
		pass

def format_coord(in_lat, in_lon):
	'''
	TBD:
	takes in a latitude and a longitude in 
	returns a nicely formatted string in degrees minutes seconds
	'''
	out_lat = in_lat
	out_lon = in_lon
	return (out_lat, out_lon)

def handlegpsdata():
	'''
	Read GPS
	if we get valid data, blink the LED, return True
			and save the info
	else return False
	'''

	try:
		g.read()
		if g.lat != -1.0:
			display( "valid GPS data",in_lcd=False)
			return True

	except KeyboardInterrupt:
		sys.exit()
	except:
		pass
	display( "invalid GPS data",in_lcd=True)
	return False
	
def handledhtdata():
	global temp, hum
	[ temp, hum ] = grovepi.dht(dht_sensor_port,dht_sensor_type)
	if temp != -1 and hum != -1:
		display("temp = {}C    humidity={}%".format(temp,hum),(0,255,0))
	else:	
		display("Error reading DTH sensor")

def logtofile():
	try:
		fobj = open( logfile,"a")
		fobj.write("#{:3d},{:.4f}, {:.4f}, {}, {:.2f}, {:.2f}%\n".format(
			count,g.latitude,g.longitude, g.timestamp, temp,hum))
		fobj.flush()
		fobj.close()
	except KeyboardInterrupt:
		sys.exit()
	except:
		display("Error writing to USB Drive",in_lcd=True)
		time.sleep(3)

	# handle time. Convert according to timezone
	# convert timestamp to struct_time
	#my_time = time.strptime(g.timestamp,"%H%M%S.000")  
	#print my_time

def savephoto():
	try:
		photoname = photo_location+str(g.timestamp)+".jpg"
		display( photoname,in_lcd=False)
		cam.capture(photoname)
		grovepi.digitalWrite(led,0)
		time.sleep(1)
		grovepi.digitalWrite(led,255)
			
		# Get ready to watermark the image
		
		# 1. grab the image
		base = Image.open(photoname).convert('RGBA')

		# 2. create overlay
		txt = Image.new('RGBA', base.size, (255,255,255,50))
		# get a drawing context
		d = ImageDraw.Draw(txt)

		# 3. prepare text to overlay
		d.text((20,overlay_txt_ypos), 
			"#{}: lon: {:.4f} lat: {:.4f} temp: {:.1f}C humidity: {:.1f}%".format(
			count,g.longitude,g.latitude, temp,hum), font=fnt, fill=(255,255,255,255))
		
		# 4. do composite and save
		out = Image.alpha_composite(base, txt)
		out.save(photoname)
		grovepi.digitalWrite(led,255)
	except KeyboardInterrupt:
		sys.exit()
	except:
		display("Error saving photo",in_lcd=True)
		time.sleep(3)




###############################################################


try:
	display("Starting up...",in_lcd=True)
	grovepi.digitalWrite(led,0)
except:
	pass

# check camera
try:
	g = grovegps.GROVEGPS()
	cam = picamera.PiCamera(sensor_mode=3)
	display("Camera working",in_lcd=True)
except:
	display("Camera NOT working!!",in_lcd=True)

# get a font
fnt = ImageFont.truetype('/usr/share/fonts/truetype/roboto/Roboto-Thin.ttf', 20)
count = 0
while True:

	if handlegpsdata():
		count += 1
		grovepi.digitalWrite(led,255)
		display("{} {}, {} {}, {}, {}".format(g.lat,g.NS,g.lon,g.EW, g.latitude,g.longitude),
			in_lcd=False)
		handledhtdata()
		savephoto()
		logtofile()
		time.sleep(5)
		display("lon: {:11.7f}lat: {:11.7f}".format(g.longitude,g.latitude),(0,0,255))
	time.sleep(5)
	grovepi.digitalWrite(led,0)



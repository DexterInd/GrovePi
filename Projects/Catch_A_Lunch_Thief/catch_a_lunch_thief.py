#! /usr/local/bin/python
# This project by Dexter Industries will help you figure out who's stealing your lunch!  In 
# this project, we will use the GrovePi to take a picture of the culprit when the light in 
# your fridge turns on.  We will use the light detector for Grove to detect when the fridge
# door has been opened.
#
# Hardware Setup: 
# - Use the Raspberry Pi and GrovePi.  	(http://www.dexterindustries.com/shop/grovepi-starter-kit-2/)
# - Use the Raspberry Pi camera.	(http://www.dexterindustries.com/shop/raspberry-pi-camera/)
# - Connect the light sensor to A0. (http://www.dexterindustries.com/shop/grove-light-sensor/)
# You can adjust the threshold value if you have a bright environment.  
# Change the email_destination to change the destination you send an e-mail to.  

import time
import datetime
import grovepi
import picamera
import send_email_pic

email_destination = 'examples@dexterindustries.com'		# Change this to the destination e-mail.
destination = [email_destination] 						# We put it into an array.

# Connect the Grove Light Sensor to analog port A0
# SIG,NC,VCC,GND
light_sensor = 0										# Connect the light sensor to A0 Port.
grovepi.pinMode(light_sensor,"INPUT")					# Set the A0 port to input.

# Send a picture once sensor exceeds threshold resistance
threshold = 600											# Adjust this threshold higher or lower
														# Depending on how bright your fridge is.

camera = picamera.PiCamera()							# Setup the Pi Camera

# Simple function to get the date as a string.
def get_time_string():
    dateString = '%Y-%m-%d_%H-%M-%S'
    return_string = datetime.datetime.now().strftime(dateString)
    return return_string

while True:
    try:
        # Get sensor value.  Read the light sensor.
        sensor_value = grovepi.analogRead(light_sensor)

        # Sense the light coming on, within the target range
        if sensor_value > threshold:
            print ('The fridget light is on!')	# Print a note to let us know how it goes.
            file_name = "lunch_status-"+str(get_time_string())+".jpg"
            camera.capture(file_name)			# Take a picture and save it to file_name
            # Now send an e-mail
            send_email_pic.send_email("The fridge has been opened!", destination, "The fridge has been opened!", file_name)
        else:
            print ('.')	# Do nothing!  It's still dark.
        
        time.sleep(.5)	# If your hold time is less than this, you might not see as many detections

    except IOError:
        print ("Error")

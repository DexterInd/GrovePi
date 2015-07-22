# Detects motion, triggers Buzzer, LED and Relay, takes picture from RPi Camera, sends as attachment via Gmail
# http://www.dexterindustries.com/GrovePi/projects-for-the-raspberry-pi/whos-at-the-door/

# GrovePi + Ultrasonic Ranger + Buzzer + Switch + Relay + LED + RPi Camera
# http://www.seeedstudio.com/wiki/Grove_-_Ultrasonic_Ranger
# http://www.seeedstudio.com/wiki/Grove_-_Buzzer
# http://www.seeedstudio.com/wiki/Grove_-_Switch(P)
# http://www.seeedstudio.com/wiki/Grove_-_Solid_State_Relay
# http://www.seeedstudio.com/wiki/Grove_-_LED_Socket_Kit
# http://www.raspberrypi.org/camera

'''
## License
 GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
 Copyright (C) 2015  Dexter Industries

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.
'''

import grovepi
# Import smtplib for the actual sending function
import smtplib, string, subprocess, time

# Here are the email package modules we'll need
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from subprocess import call

print "System Working"
switch = 4
led_status = 3
relay = 2
buzzer = 5

SMTP_USERNAME = ''  # Mail id of the sender
SMTP_PASSWORD = ''  # Pasword of the sender
SMTP_RECIPIENT = '' # Mail id of the reciever
SMTP_SERVER = 'smtp.gmail.com'  # Address of the SMTP server
SSL_PORT = 465

while True:     # in case of IO error, restart
    try:
        grovepi.pinMode(switch,"INPUT")
        while True:
            if grovepi.digitalRead(switch) == 1:    # If the system is ON
                if grovepi.ultrasonicRead() < 100:  # If a person walks through the door
                    print "Welcome"
                    grovepi.analogWrite(buzzer,100) # Make a sound on the Buzzer
                    time.sleep(.5)
                    grovepi.analogWrite(buzzer,0)       # Turn off the Buzzer
                    grovepi.digitalWrite(led_status,1)  # Turn on the status LED to indicate that someone has arrived
                    grovepi.digitalWrite(relay,1)       # turn on the Relay to activate an electrical device

                    # Take a picture from the Raspberry Pi camera
                    call (["raspistill -o i1.jpg -w 640 -h 480 -t 0"], shell=True)
                    print "Image Shot"
                    p = subprocess.Popen(["runlevel"], stdout=subprocess.PIPE)
                    out, err=p.communicate()    # Connect to the mail server
                    if out[2] == '0':
                        print 'Halt detected'
                        exit(0)
                    if out [2] == '6':
                        print 'Shutdown detected'
                        exit(0)
                    print "Connected to mail"

                    # Create the container (outer) email message
                    TO = SMTP_RECIPIENT
                    FROM = SMTP_USERNAME
                    msg = MIMEMultipart()
                    msg.preamble = 'Rpi Sends image'

                    # Attach the image
                    fp = open('i1.jpg', 'rb')
                    img = MIMEImage(fp.read())
                    fp.close()
                    msg.attach(img)

                    # Send the email via Gmail
                    print "Sending the mail"
                    server = smtplib.SMTP_SSL(SMTP_SERVER, SSL_PORT)
                    server.login(SMTP_USERNAME, SMTP_PASSWORD)
                    server.sendmail(FROM, [TO], msg.as_string())
                    server.quit()
                    print "Mail sent"

                    grovepi.digitalWrite(led_status,0)  # Turn off the LED
                    grovepi.digitalWrite(relay,0)       # Turn off the Relay
    except IOError:
        print "Error"

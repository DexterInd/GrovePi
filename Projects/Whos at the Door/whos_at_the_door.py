# Detects motion, triggers Buzzer, LED and Relay, takes picture from RPi Camera, sends as attachment via Gmail
# http://www.dexterindustries.com/GrovePi/projects-for-the-raspberry-pi/whos-at-the-door/

# GrovePi + Ultrasonic Ranger + Buzzer + Switch + Relay + LED + RPi Camera
# http://www.seeedstudio.com/wiki/Grove_-_Ultrasonic_Ranger
# http://www.seeedstudio.com/wiki/Grove_-_Buzzer
# http://www.seeedstudio.com/wiki/Grove_-_Switch(P)
# http://www.seeedstudio.com/wiki/Grove_-_Solid_State_Relay
# http://www.seeedstudio.com/wiki/Grove_-_LED_Socket_Kit
# http://www.raspberrypi.org/camera

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

#! /usr/local/bin/python
# This example will show you how to send an email in python, with a picture
# attachment.  This example uses outlook.com to send an e-mail.

SMTPserver = 'smtp.live.com' 
sender = 'dexterexamples@outlook.com' 

USERNAME = "dexterexamples@outlook.com" 
PASSWORD = "password"

text_subtype = 'plain'  # typical values for text_subtype are plain, html, xml
content="""\ Test message """ 
import sys 
import os 
import re

# from smtplib import SMTP_SSL as SMTP # this invokes the secure SMTP 
# protocol (port 465, uses SSL)

from smtplib import * 
from smtplib import SMTP 				# use this for standard SMTP protocol (port 25, no encryption) 
from email.MIMEText import MIMEText
# Here are the email package modules we'll need for images.
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

def send_email(content, destination, subject, file):
    try:
        msg = MIMEMultipart()
        msg['Subject']= subject
        msg['From'] = sender # some SMTP servers will do this automatically, not all

        fp = open(file, 'rb')				# Open File name "file"
        img = MIMEImage(fp.read())			# Read the file.
        fp.close()							# Good housekeeping: close the file.
        msg.attach(img)						# Attach the file to the message.

        conn = SMTP(SMTPserver, port = 587, timeout = 60)          # timeout is critical here for long term health.
        conn.ehlo()
        conn.starttls()
        conn.ehlo()
        conn.login(USERNAME, PASSWORD)
        conn.set_debuglevel(1)
        try:
            conn.sendmail(sender, destination, msg.as_string())
        finally:
            conn.close()
    except Exception as exc:
        # Print a message error!
        print("Mail failed; %s" % str(exc))
        print("Moving on!")

# Example function call!  This is what calling the function would look like!
# send_email(content, destination, subject, file)  where "content" is the content of the email, destination is the destination 
# of the e-mail (who you're emailing to) and subject is the subject of the e-mail.  file is the filename of the image file
# you want to attach.  It's usually best to include the full path of the file!
file = "/home/pi/test.jpg"
destination = ['examples@dexterindustries.com'] 	# Enter the destination e-mail address here, between the ''
send_email("Hello from my Raspberry Pi!", destination, "Hello from Dex!", file)

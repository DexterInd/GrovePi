#! /usr/local/bin/python

# This is an example of sending an e-mail with the Raspberry Pi.  This is a very
# useful example, if you want to send an e-mail or alert on some hardware change!
# In this example we use a hotmail/outlook account.  Settings may vary depending
# on the e-mail provider you are using.  
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  
# You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  
# Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

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

SMTPserver = 'smtp.live.com'		# This is the SMTP server.  In our example, we use Microsoft Outlook.
sender =     'dex@outlook.com'				# This is your login email.
destination = ['dex@dexterindustries.com']	# This is the e-mail address you want to send an e-mail to.  
											# You can send to multiple e-mails.  The e-mail address is a string.

USERNAME = "dex@outlook.com"
PASSWORD = "my_password"

# typical values for text_subtype are plain, html, xml
text_subtype = 'plain'

content="""\
Test message
"""

import sys
import os
import re

# from smtplib import SMTP_SSL as SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)
from smtplib import *
from smtplib import SMTP                  # use this for standard SMTP protocol   (port 25, no encryption)
from email.MIMEText import MIMEText

#
def send_email(content, destination, subject):
    try:
        msg = MIMEText(content, text_subtype)
        msg['Subject']=       subject
        msg['From']   = sender # some SMTP servers will do this automatically, not all

        # timeout is critical here for long term health.  
        conn = SMTP(SMTPserver, port = 587, timeout = 60)
        
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
        # sys.exit( "mail failed; %s" % str(exc) ) # give a error message
        print("Mail failed; %s" % str(exc))
        print("Moving on!")

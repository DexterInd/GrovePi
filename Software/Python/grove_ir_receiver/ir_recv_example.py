#!/usr/bin/env python
##################################################
# IR remote control example
#
# This example is for controlling the GrovePi with an Keyes IR remote
# 
# History
# ------------------------------------------------
# Author	Date      		Comments
# Karan		21 Aug  15	  	Initial Authoring
#
# Have a question?  Please ask on our forums!  http://forum.dexterindustries.com/c/grovepi
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2015  Dexter Industries

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
##################################################
import lirc
#initialize the IR daemon
sockid = lirc.init("keyes", blocking = False)
while True:
	#Wait for the next IR code to arrive. The codes are queued in a buffer before printing
	a= lirc.nextcode()  
	if len(a) !=0:
		print(a[0])
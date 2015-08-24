#!/usr/bin/env python
##################################################
# IR remote control example
#
# This example is for controlling the GoPiGo with an Keyes IR remote
# 
# History
# ------------------------------------------------
# Author	Date      		Comments
# Karan		21 Aug  15	  	Initial Authoring
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)      
##################################################
import lirc
#initialize the IR daemon
sockid = lirc.init("keyes", blocking = False)
while True:
	#Wait for the next IR code to arrive. The codes are queued in a buffer before printing
	a= lirc.nextcode()  
	if len(a) !=0:
		print a[0]
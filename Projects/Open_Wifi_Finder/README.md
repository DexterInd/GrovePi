## **GrovePi Open Wifi Finder**

GrovePi is an open source platform for connecting Grove Sensors to the Raspberry Pi.  Create your Internet of Things devices and inventions, no soldering!

Scan for open wifi networks!  This is a portable wifi hotspot finder.  See our project [here](http://www.dexterindustries.com/GrovePi) for more information on turning this into a portable wifi hotspot finder.

### How Does it Work?
The GrovePi board slips over the Raspberry Pi.  Connect the Grove Sensors to the GrovePi board.  

####Software Setup Notes:
  * This example uses [wifi library](https://wifi.readthedocs.org/en/latest/wifi_command.html).  Install with pip install wifi
  * Wifi dongle must be on wlan0 ; Check this with the command "ifconfig" on the command line.

####Hardware Setup Notes:
  * Buzzer goes on port D2 of the GrovePi.
  * LED Goes on port D3 of the GrovePi.
  * The LCD goes on I2C-1.  Check this with the command "sudo i2cdetect -y 1"

The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn [more about GrovePi here.](http://www.dexterindustries.com/GrovePi)

### Make This Start at Boot!
If you're going to take this outside, make sure you can start this at boot.  
 
First, the files in this directory are copied into the home directory.
 
Make a script "start.sh" and put a command to start the wifi_finder.py script.
 
```
sudo nano start.sh
```
 
The contents of start.sh are going to be:
 
```
#!/bin/bash
sudo python /home/pi/wifi_finder.py
```

And then open up rc.local

```
sudo nano /etc/rc.local
```

and add the last few lines of this file should be:

```
sudo sh /home/pi/start.sh
exit 0
```

Then that's it!  Reboot and test!
 
Have a question about this example?  [Ask on the forums here.](http://forum.dexterindustries.com/c/grovepi)

LICENSE: 
These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.


### Raspberry Pi Compatibility
The GrovePi is compatible with the Raspberry Pi models A, A+, B, B+, and 2.

### Programming the GrovePi
The GrovePi can be programmed in Python, C, C#, Go, and NodeJS on the Raspberry Pi.  Simply start with one of our [example projects](http://www.dexterindustries.com/GrovePi/projects-for-the-raspberry-pi/) or [example code](https://github.com/DexterInd/GrovePi/tree/master/Software).  
The GrovePi uses an Arduino to interface between the Raspberry Pi and the Grove Sensors, and comes programmed with a standard firmware.  The firmware can be rewritten from the Raspberry Pi.  

### Getting Help
Need help? We [have a forum here where you can ask questions or make suggestions](http://www.dexterindustries.com/GrovePi/projects-for-the-raspberry-pi/).

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


See more at the [GrovePi Site](http://dexterindustries.com/GrovePi/)

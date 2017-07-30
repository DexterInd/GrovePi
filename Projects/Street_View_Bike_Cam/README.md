This project was created for the GrovePi0 as an example of a portable project

![alt text](http://32414320wji53mwwch1u68ce.wpengine.netdna-cdn.com/wp-content/uploads/2016/07/20160703_144803-1024x576.jpg "Pi on a Bike")
You can equip your bike with a GPS logger, which will take a photo every minute, 
and stamp it with the GPS coordinates, and temperature/humidity data.
Project is documented at http://www.dexterindustries.com/projects/take-grovepizero-bike-trip/

You will need a Pizero with a Pi camera (it requires a special cable for the pizero),
you will need to run Cinch on your SD card
The GPS sensor goes into port RPISER
The temperature/humidity sensor goes into port D3
An optional LCD screen goes into one of the I2C ports.

You will also need to make a copy of the dextergps.py library into this folder. 
You can find that file in **GrovePi/Software/Python/grove_gps/**

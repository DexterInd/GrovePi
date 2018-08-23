GrovePi Examples for using the [Grove GPS Module](http://www.seeedstudio.com/depot/Grove-GPS-p-959.html?cPath=25_130)

*Files*:
- grove_gps_hardware_test.py : This example is for is the simplest GPS Script.  It simply reads the raw output of the GPS sensor on the GoPiGo or GrovePi and prints it. 
- grove_gps_data.py : Reads and parses the data for individual elements like the lat, long and other variables
- GroveGPS.py is the basic library from Seeed
- dextergps.py is the newest library. The challenge with GPS data is parsing the incoming data to get appropriate valid information out of it. dextergps.py uses regular expressions to ensure data validity and is quite simple to use:
```python
	gps = GROVEGPS()
	while True:
		time.sleep(1)
		in_data = gps.read()
		if in_data != []:
			print in_data
      print gps.lat, gps.NS, gps.lon,gps.EW
      print gps.latitude, gps.longitude
```

**gps.lat** and **gps.NS** go hand in hand, so do **gps.lon** and **gps.EW**

**gps.latitude** and **gps.longitude** are calculated to give you a Google Map appropriate format and make use of negative numbers to indicate either South or West

*Note*:
You would only get good data when fix is 1 and you have 3 or more satellites in view. You might have to take the module near a window with access to open sky for good results

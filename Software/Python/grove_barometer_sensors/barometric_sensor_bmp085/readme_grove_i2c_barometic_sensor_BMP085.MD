This is a Python 2.7 script wich can be used to get readings from the Grove Digital Barometic Sensor(BMP085) (http://www.seeedstudio.com/depot/Grove-Barometer-Sensor-p-1199.html) connected to the GrovePi on a Raspberry Pi.

The script Grove_Barometic_Sensor.py containes a class BMP085 (this is the actual sensor-chip on the device). All functions are inside this class and can be called from other scripts if you set the following code in the script:
	from Grove_Barometic_Sensor import BMP085

If you set debug = True in the def__init__ function it displays all calculations on screen. If you set debug = False, the script just runs and sends the output to the calling script.

The script reads the raw temperature and raw pressure from the sensor. It then performs some calculations to transform the readed temperature to  a calbrated temperature in °C and to perform a compenstion to the readed pressure to changed it to a calibrated value in Pascal. Finaly it calculates the altitude in meters above sea level using the barometric hight formula (sea http://en.wikipedia.org/wiki/Atmospheric_pressure). Standard it uses the sea level standard atmospheric pressure 101329 Pa. If you want to use a local sea level pressure, call the function readAltitude(123456) with the correct value between brackryd (make sure to give the value in Pascal (or multiply the value in hPa by 100)).

The script works in 4 modes (depending on how the initialisations is done in the calling script: 
0 ULTRA LOW POWER Mode
1 Standard Mode
2 HIRES Mode
3 ULTRAHIRES Mode

If you need a value of the pressure in hPa, make sure to divide the returned value by 100 in the calling script.

September 2014.
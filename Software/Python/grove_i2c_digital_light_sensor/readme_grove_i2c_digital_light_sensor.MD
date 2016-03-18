This is a Python 2.7 script which can be used to get readings from the Grove Digital Light Sensor(http://www.seeedstudio.com/wiki/Grove_-_Digital_Light_Sensor) connected to the GrovePi on a Raspberry Pi.

If you set debug = 1 (standard option) it displays all calculations on screen.
If you set debug = 0, the script just runs and only displays the output.

The script get's both the IR-reading and ambient reading from the sensor. It then scales the the readings and calculates the lux-value.

the main function performs a continuous loop, gets the readings and calculated lux-value and displays the result (depending on the result the output can be normal values and a message 'it's light' or 'it's dark' or a message if the sensor is saturated and no values can be achieved. The loop is repeated with a time.sleep(10) so you can easily read the result on screen.

If your not interested in the IR or ambient values but just want the lux value, comment out the undisered output lines. Be sure not to comment out the reading and calculating lines in the different functions because you need both the IR and the ambient values in order to calculate the lux value.

September 2014.
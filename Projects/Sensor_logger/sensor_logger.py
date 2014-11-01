# Temperature levels with our Raspberry Pi


import time
import grovepi
import math
import datetime

# Connections
temperature_sensor_in = 3   # port D3
temperature_sensor_out = 4  # port D4
light_sensor = 0            # port A0 
sound_sensor = 1            # port A1

def openFile():
	try:
		now = datetime.datetime.now()
	
		f = open("log_%d_%d_%d.txt" %(now.day,now.month,now.year), "a")
		
		return f
	except IOError:
		print("File ERROR")
		openFile()

while True:
        try:
            [temp,humidity] = grovepi.dht(temperature_sensor_in,0)
            t_in = temp
            h_in = humidity

            [temp,humidity] = grovepi.dht(temperature_sensor_out,1)
            t_out = temp
            h_out = humidity
    
	    light = grovepi.analogRead(light_sensor)

            sound_level = grovepi.analogRead(sound_sensor)
            if sound_level > 0:
                last_sound = sound_level
	
            now = datetime.datetime.now()

	   # print(now.isoformat() + " || IN: " +  "Temp: %.2f, Hum: %d || OUT: Temp: %.2f, Hum: %d || Light: %d \n" %(t_in,h_in,t_out,h_out,light))
 
            f = openFile()
            f.write(now.isoformat() + " || IN: " +  "Temp: %.2f, Hum: %d || OUT: Temp: %.2f, Hum: %d || Light: %d || Sound: %d \n" %(t_in,h_in,t_out,h_out,light,last_soun,last_sound))
	    f.close()

            time.sleep(30)

        except IOError:
            pass
        except:
            f = openFile()
            f.write(now.isoformat() + "   ERROR \n")
            f.close()
            time.sleep(10)

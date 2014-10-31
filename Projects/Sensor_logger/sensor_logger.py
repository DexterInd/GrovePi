# Temperature levels with our Raspberry Pi


import time
import grovepi
import math
import datetime

# Connections
temperature_sensor_in = 3  # port D3
temperature_sensor_out = 2 # port D2
#light_sensor = 0        # port A1 



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
    
            #light_intensity = grovepi.analogRead(light_sensor)

            now = datetime.datetime.now()

            f = openFile
            #f.write(now.isoformat() + " || IN: " +  "Temp: %.2f, Hum: %d || OUT: Temp: %.2f, Hum: %d || Sound: %d \n" %(t_in,h_in,t_out,h_out,light_intensity))
			f.write(now.isoformat() + " || IN: " +  "Temp: %.2f, Hum: %d || OUT: Temp: %.2f, Hum: %d \n" %(t_in,h_in,t_out,h_out,))
            f.close()

            time.sleep(60)

        except IOError:
            pass
        except:
            f = openFile()
            f.write(now.isoformat() + "   ERROR \n")
            f.close()
            time.sleep(60)

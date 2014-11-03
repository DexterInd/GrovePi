# Temperature, Humidity, Sound, Light levels with our Raspberry Pi
# Modified by Jan
import time
import grovepi
import math
import datetime

# Connections
temperature_sensor_in = 3   # port D3
temperature_sensor_out = 4  # port D4
light_sensor = 0            # port A0 
sound_sensor = 1            # port A1

last_sound = 0

temp_in_max = -20
temp_in_min = 40

temp_out_max = -20
temp_out_min = 40

current_hour = 0

def openFile():
	try:
		now = datetime.datetime.now()
	
		file = open("log_%d_%d_%d.txt" %(now.day,now.month,now.year), "a")
		
		return file
	except IOError:
		print("File ERROR")
		openFile()

def writeAverage(log_file):
        
        now = datetime.datetime.now()
        
        if current_hour != now.hour:
            current_hour = now.hour
            log_file.write("HOUR: %d MIN / MAX TEMPS: ||| IN: %.2f / %.2f ||| OUT: %.2f / %.2f \n" %(current_hour,temp_in_min,temp_in_max,temp_out_min,temp_out_max))  

while True:
        try:
		[temp,humidity] = grovepi.dht(temperature_sensor_in,0)
		t_in = temp
		h_in = humidity
			
		if t_in > temp_in_max:
			temp_in_max = t_in
		elif t_in < temp_in_min:
			temp_in_min = t_in

		[temp,humidity] = grovepi.dht(temperature_sensor_out,1)
           	t_out = temp
           	h_out = humidity
			
		if t_out > temp_out_max:
			temp_out_max = t_out
		elif t_out < temp_out_min:
			temp_out_min = t_out
			
			
		light = grovepi.analogRead(light_sensor)

        	sound_level = grovepi.analogRead(sound_sensor)
		if sound_level > 0:
	                last_sound = sound_level
	
            	now = datetime.datetime.now()
 
            	log_file = openFile()
			
            	log_file.write(now.isoformat() + " || IN: " +  "Temp: %.2f, Hum: %d || OUT: Temp: %.2f, Hum: %d || Light: %d || Sound: %d \n" %(t_in,h_in,t_out,h_out,light,last_sound))
		# writeAverage(log_file)
                
                if current_hour != now.hour:
                    current_hour = now.hour
                    log_file.write("%d MIN / MAX TEMPS: ||| IN: %.2f / %.2f ||| OUT: %.2f / %.2f \n" %(current_hour,temp_in_min,temp_in_max,temp_out_min,temp_out_max))  


		log_file.close()

        	time.sleep(30)

        except IOError:
		 pass
        except:
		f = openFile()
            	f.write(now.isoformat() + "   ERROR \n")
            	f.close()
            	time.sleep(10)

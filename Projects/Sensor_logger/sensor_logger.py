# Temperature, Humidity, Sound, Light levels with our Raspberry Pi
# Modified by Jan
import time
import grovepi
import datetime
import traceback

# Connection
temperature_sensor_in = 3   # port D3
temperature_sensor_out = 4  # port D4
light_sensor = 0			# port A0
sound_sensor = 1			# port A1

global i_last_sound

global f_temp_out_max
global f_temp_in_min

global f_temp_out_max
global f_temp_out_min

global i_current_hour


def init():
    global i_last_sound
    global f_temp_out_max
    global f_temp_in_min

    global f_temp_out_max
    global f_temp_out_min

    global i_current_hour

    try:
        [temp,humidity] = grovepi.dht(temperature_sensor_in,0)
        f_temp_out_max = temp
        f_temp_in_min = temp

        [temp,humidity] = grovepi.dht(temperature_sensor_out,1)
        f_temp_out_max = temp
        f_temp_out_min = temp

        i_last_sound  = grovepi.analogRead(sound_sensor)

        i_current_hour = datetime.datetime.now().hour

    except:
        error(" init")
        init()

def error(err_message):
    time_now = datetime.datetime.now()
	
    write_file("logs/log_err_%d_%d_%d.txt" %(time_now.day,time_now.month,time_now.year),
                   time_now.isoformat() + "   ERROR" + err_message + "\n")


def write_file(str_log_name ,str_log_write):
    try:

        file = open(str_log_name, "a")
        file.write(str_log_write)
        file.close()

    except IOError:
        print("File ERROR")
        write_file(str_log_name ,str_log_write)

def write_val_file(str_log_name ,str_log_write):
      try:

        file = open(str_log_name, "w")
        file.write(str_log_write)
        file.close()

      except IOError:
        print("Value File ERROR")
        write_file(str_log_name ,str_log_write)


def writeMinMax():
    global i_current_hour
    time_now = datetime.datetime.now()

    if i_current_hour != time_now.hour:
        i_current_hour = time_now.hour
        write_file("logs/log_%d_%d_%d.txt" %(time_now.day,time_now.month,time_now.year),
                   "HOUR: %d MIN / MAX TEMPS: ||| IN: %.2f / %.2f ||| OUT: %.2f / %.2f \n" %(i_current_hour,f_temp_in_min,f_temp_out_max,f_temp_out_min,f_temp_out_max))
        init()

def writeSingleValues(temp_in, temp_out ,hum_in ,hum_out ,light ,last_sound):
    write_val_file("values/temp_in", "%.2f" %(temp_in))
    write_val_file("values/temp_out", "%.2f" %(temp_out))
    write_val_file("values/hum_in", "%d" %(hum_in))
    write_val_file("values/hum_out", "%d" %(hum_out))
    write_val_file("values/light", "%d" %(light))
    write_val_file("values/last_sound", "%d" %(last_sound))


init()

while True:
    try:
        [temp,humidity] = grovepi.dht(temperature_sensor_in,0)
        t_in = temp
        h_in = humidity

        if t_in > f_temp_out_max:
            f_temp_out_max = t_in
        elif t_in < f_temp_in_min:
            f_temp_in_min = t_in
        
        [temp,humidity] = grovepi.dht(temperature_sensor_out,1)
        t_out = temp
        h_out = humidity

        if t_out > f_temp_out_max:
            f_temp_out_max = t_out
        elif t_out < f_temp_out_min:
            f_temp_out_min = t_out
	
        light = grovepi.analogRead(light_sensor)


        sound_level = grovepi.analogRead(sound_sensor)
        if sound_level > 0:
            i_last_sound = sound_level
					
        time_now = datetime.datetime.now()

        write_file("logs/log_%d_%d_%d.txt" %(time_now.day,time_now.month,time_now.year),
                              time_now.isoformat() + " || IN: " +  "Temp: %.2f, Hum: %.0f || OUT: Temp: %.2f, Hum: %.0f || Light: %d || Sound: %d \n" %(t_in,h_in,t_out,h_out,light,i_last_sound))
	 
        writeSingleValues(t_in, t_out, h_in, h_out, light, i_last_sound)

        writeMinMax()
		
        time.sleep(30)
    except IOError:
        pass
    except:
        error(" Running" + traceback.format_exc())
        time.sleep(10)

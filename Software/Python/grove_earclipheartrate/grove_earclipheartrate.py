# Code contributed by Alessandro Graps a.graps@joulehub.com
# May 2020
# Many thanks !!! 

from datetime import datetime

from datetime import timedelta
import time
import grovepi

# Connect the Grove Ear Clip Sensor to digital port D3
sensorPin = 3
start_time = datetime.now()
counter = 0
temp = [0] * 21
data_effect = True
heart_rate = 0
max_heartpulse_duty = 2000
    
def millis():
   global start_time
   dt = datetime.now() - start_time
   ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0

   return ms

def arrayInit():  
    global temp
    global counter
    counter = 0
    temp = [0] * 21
    temp[20] = millis()

def sum():                               
    global heart_rate, temp, data_effect
    if data_effect:
        heart_rate=1200000/(temp[20]-temp[0]);
    
def interrupt():
    global counter
    global temp
    global data_effect
    
    temp[counter] = millis()
    
    if counter == 0:       
        sub = temp[counter]-temp[20]
    else:
        sub = temp[counter]-temp[counter-1]

    if sub > max_heartpulse_duty:
        data_effect = False
        counter = 0
        arrayInit()
    if counter == 20 and data_effect:
        counter = 0
        sum()
    elif counter != 20 and data_effect:
        counter += 1
    else: 
        counter = 0
        data_effect = True

def main():

    global heart_rate
    
    print("Please place the sensor correctly")
    time.sleep(4)
    print("Starting measurement...")
    arrayInit()
    grovepi.set_pin_interrupt(sensorPin, grovepi.COUNT_CHANGES, grovepi.RISING, 1000)





    while True:
        value = grovepi.read_interrupt_state(sensorPin)
        if value > 0:
            interrupt()
        time.sleep(0.73)
        print("HR: {:2.0f}".format(heart_rate))
     
 
if __name__ == '__main__':
    main()

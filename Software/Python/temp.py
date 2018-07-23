from time import sleep # we need to use the sleep function to delay readings
import datetime # that's for printing the current date
import time
import grovepi
import math
import json

dht_sensor = 4
ultrasonic_ranger = 6
light_sensor = 0
sound_sensor = 1
button = 3
ir = 5

grovepi.pinMode(sound_sensor,"INPUT")
grovepi.pinMode(button,"INPUT")
grovepi.pinMode(light_sensor,"INPUT")
grovepi.dust_sensor_en()
grovepi.setDustSensorInterval(5000)
# grovepi.ir_recv_pin(ir)

data = {
    'sound': 0,
    'light': 0,
    'button': 0,
    'temp': 0,
    'humidity': 0,
    'prox': 0,
    'dust': 0
}

while True:
    data['sound'] = grovepi.analogRead(sound_sensor)
    data['light'] = grovepi.analogRead(light_sensor)
    [data['temp'],data['humidity']] = grovepi.dht(dht_sensor,0)
    data['button'] = grovepi.digitalRead(button)
    data['prox'] = grovepi.ultrasonicRead(ultrasonic_ranger)
    data['dust'] = grovepi.dustSensorRead()
    print(json.dumps(data))

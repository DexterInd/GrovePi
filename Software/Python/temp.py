from time import sleep # we need to use the sleep function to delay readings
import datetime # that's for printing the current date
import time
import grovepi
import math
import json

dht_sensor = 7
ultrasonic_ranger = 5
light_sensor = 0
sound_sensor = 1
button = 6
led = 3
ledbar = 4
ir = 8

val = 0

# grovepi.additional_waiting = 0.005
grovepi.pinMode(sound_sensor,"INPUT")
grovepi.pinMode(button,"INPUT")
grovepi.pinMode(light_sensor,"INPUT")
grovepi.pinMode(led, "OUTPUT")
grovepi.dust_sensor_en()
grovepi.setDustSensorInterval(5000)
grovepi.ir_recv_pin(ir)
# grovepi.ledBar_init(ledbar, 0)

data = {
    'sound': 0,
    'light': 0,
    'button': 0,
    'temp': 0,
    'humidity': 0,
    'prox': 0,
    'dust': 0,
    'ir': 3 * [0]
}

while True:
    data['sound'] = grovepi.analogRead(sound_sensor)
    data['light'] = grovepi.analogRead(light_sensor)
    # [data['temp'],data['humidity']] = grovepi.dht(dht_sensor,0)
    data['button'] = grovepi.digitalRead(button)
    data['prox'] = grovepi.ultrasonicRead(ultrasonic_ranger)
    data['dust'] = grovepi.dustSensorRead()
    grovepi.analogWrite(led, val % 256)
    # grovepi.ledBar_setBits(ledbar, val % 1024)
    if grovepi.ir_is_data():
        data['ir'] = list(grovepi.ir_read_signal())
    val += 10
    print(json.dumps(data))
    time.sleep(0.2)

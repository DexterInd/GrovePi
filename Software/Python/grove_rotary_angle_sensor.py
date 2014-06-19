# GrovePi + Rotary Angle Sensor (Potentiometer) + LED
# http://www.seeedstudio.com/wiki/Grove_-_Rotary_Angle_Sensor
# http://www.seeedstudio.com/wiki/Grove_-_LED_Socket_Kit

import time
import grovepi

# Connect the Rotary Angle Sensor to analog port A0
potentiometer = 0

# Connect the LED to digital port D5
led = 5

grovepi.pinMode(potentiometer,"INPUT")
grovepi.pinMode(led,"OUTPUT")
time.sleep(1)

# Reference voltage of ADC is 5v
adc_ref = 5

# Vcc of the grove interface is normally 5v
grove_vcc = 5

# Full value of the rotary angle is 300 degrees, as per it's specs (0 to 300)
full_angle = 300

while True:
    try:
        # Read sensor value from potentiometer
        sensor_value = grovepi.analogRead(potentiometer)

        # Calculate voltage
        voltage = (float)sensor_value * adc_ref / 1023;

        # Calculate rotation in degrees (0 to 300)
        degrees = (voltage * full_angle) / grove_vcc;

        # Calculate LED brightess (0 to 255) from degrees (0 to 300)
        brightness = (degrees / full_angle) * 255

        # Give PWM output to LED
        grovepi.analogWrite(led,brightness)

    except IOError:
        print "Error"

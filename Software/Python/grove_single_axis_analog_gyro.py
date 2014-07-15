# GrovePi + Grove Single Axis Analog Gyro
# http://www.seeedstudio.com/wiki/Grove_-_Single_Axis_Analog_Gyro

import time
import grovepi

# Connect the Grove Single Axis Analog Gyro to analog port A0
# SIG,NC,VCC,GND
sensor = 0

grovepi.pinMode(sensor,"INPUT")

# calibration
print "calibrating..."
sum = 0
errors = 0
for x in range(0, 100):
    try:
        # Get sensor value
        v = grovepi.analogRead(sensor)
        sum += v
        #time.sleep(.05)
    except IOError:
        print "Error"
        errors += 1

if errors == 100:
    print "unable to calibrate"
    raise SystemExit

reference_value = sum / (100 - errors)

print "finished calibrating"
print "reference_value =", reference_value

# ready
while True:
    try:
        # Get sensor value
        sensor_value = grovepi.analogRead(sensor)

        # Calculate angular velocity (deg/s)
        velocity = ((float)(sensor_value - reference_value) * 4930.0) / 1023.0 / 0.67

        print "sensor_value =", sensor_value, " velocity =", velocity
        time.sleep(.5)

    except IOError:
        print "Error"

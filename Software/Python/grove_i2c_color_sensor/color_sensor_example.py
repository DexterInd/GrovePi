import time
import grove_i2c_color_sensor

# Open connection to sensor
color_sensor = grove_i2c_color_sensor.GroveI2CColorSensor()

# Perform continuous integration
color_sensor.use_continuous_integration(100)
color_sensor.set_gain_and_prescaler(16)
color_sensor.start_integration()
time.sleep(0.15)
if color_sensor.is_integration_complete():
    print "Continuous integration complete"
    print color_sensor.read_rgbc()
    print color_sensor.read_xy()
    print color_sensor.read_color_name()
else:
    print "Continuous integration incomplete"

color_sensor.stop_integration()

# Perform manual integration
color_sensor.use_manual_integration()
color_sensor.set_gain_and_prescaler(4)
color_sensor.start_integration()
time.sleep(2)
color_sensor.stop_integration()
time.sleep(0.15)

if color_sensor.is_integration_complete():
    print "Manual integration complete"
    print color_sensor.read_rgbc()
    print color_sensor.read_xy()
    print color_sensor.read_color_name()
else:
    print "Manuel integration incomplete"

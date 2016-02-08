import time
import grove_i2c_color_sensor


color_sensor = grove_i2c_color_sensor.GroveI2CColorSensor()

# Perform continuous integration
color_sensor.use_continuous_integration(100)
color_sensor.set_gain_and_prescaler(16)
color_sensor.start_integration()
time.sleep(0.15)

print color_sensor.read_rgbc()
print color_sensor.read_xy()
print color_sensor.read_color_name()

color_sensor.stop_integration()

# Perform manual integration
color_sensor.use_manual_integration()
color_sensor.set_gain_and_prescaler(16)
color_sensor.start_integration()
time.sleep(0.15)

print color_sensor.read_rgbc()
print color_sensor.read_xy()
print color_sensor.read_color_name()
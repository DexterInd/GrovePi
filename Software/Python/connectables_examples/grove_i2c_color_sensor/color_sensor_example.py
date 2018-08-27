import time
import grove_i2c_color_sensor

# Open connection to sensor
color_sensor = grove_i2c_color_sensor.GroveI2CColorSensor()

# Perform continuous integration with predefined duration of 100ms
color_sensor.use_continuous_integration(100)
# Set gain to 16x
color_sensor.set_gain_and_prescaler(16)
# Start integration
color_sensor.start_integration()
time.sleep(.1)

if color_sensor.is_integration_complete():
    print ("Continuous integration complete. Read color:")
    color = color_sensor.read_rgbc()
    print("RGB: {},{},{} - Clear {}".format(color[0], color[1], color[2], color[3]))
    color = color_sensor.read_xy()
    print("xy: {},{}".format(color[0], color[1]))
    color = color_sensor.read_color_name()
    print("Closest color match: {}".format(color))
else:
    print("Continuous integration incomplete")

# Stop integration before changing settings
color_sensor.stop_integration()

# Perform manual integration
color_sensor.use_manual_integration()
# Set gain to 4x
color_sensor.set_gain_and_prescaler(4)
# Integrate during 200ms
color_sensor.start_integration()
time.sleep(0.2)
color_sensor.stop_integration()

if color_sensor.is_integration_complete():
    print ("Manual integration complete. Read color:")
    color = color_sensor.read_rgbc()
    print("RGB: {},{},{} - Clear {}".format(color[0], color[1], color[2], color[3]))
    color = color_sensor.read_xy()
    print("xy: {},{}".format(color[0], color[1]))
    color = color_sensor.read_color_name()
    print("Closest color match: {}".format(color))
else:
    print("Manual integration incomplete")

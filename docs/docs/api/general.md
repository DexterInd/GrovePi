#API - General Sensors

In this section the Python API reference for diverse sensors is described. This library is supported on both major versions
of Python: 2.x and 3.x.

In this section, the API for the following sensors is described:

- [Grove Temperature Sensor](http://wiki.seeedstudio.com/Grove-Temperature_Sensor_V1.2/)
- [Grove Ultrasonic Sensor](https://www.seeedstudio.com/Grove-Ultrasonic-Ranger-p-960.html)
- [DHT11](http://wiki.seeedstudio.com/Grove-TemperatureAndHumidity_Sensor/)
- [DHT22](http://wiki.seeedstudio.com/Grove-Temperature_and_Humidity_Sensor_Pro/)
- [Grove IR Receiver](https://www.seeedstudio.com/Grove-Infrared-Receiver-p-994.html) necessary for the [Infrared Remote](https://www.dexterindustries.com/shop/infrared-remote/)

---
**IMPORTANT**

This library and the other ones too are not thread-safe. You cannot call the GrovePi from multiple threads or processes
as that will put the GrovePi into a broken state.

In case you need to reset the GrovePi from your Raspberry Pi, [check this section](../fw/#resetting-the-grovepi).

The functions don't verify if the input parameters are valid and therefore the parameters have to be verified/validated before that.
Calling a function with improper parameters can result in an undefined behavior for the GrovePi.
---

##`grovepi.temp(pin, model='1.0')`
Read temperature from the [Grove Temperature Sensor](http://wiki.seeedstudio.com/Grove-Temperature_Sensor_V1.2/) on the GrovePi.

**Parameters**

- `pin {Integer}` a number to identify the port (A0-A2) from which to do the reading
- `model {String}` `"1.0"`, `"1.1"`, `"1.2"` depending on the used model

**Returns**: `{Float}` number to represent the temperature in ºC

---

##`grovepi.ultrasonicRead(pin)`
Read the distance to an object with the [Grove Ultrasonic Sensor](https://www.seeedstudio.com/Grove-Ultrasonic-Ranger-p-960.html) on the GrovePi.
The closer it is to the targeted object, the faster the sample rate and slower when it's farther.

**Parameters**

- `pin {Integer}` a number to identify the port (D2-D8) from which to do the reading

**Returns**: `{Integer}` number to represent the distance to the object in centimeters

---

##`grovepi.version()`
Read the version of the firmware.

**Returns**: a `{String}` representing the firmware version (i.e. `"1.2.7"`)

---

##`grovepi.dht(pin, module_type)`
Read the temperature and humidity on the GrovePi with one of the given modules.

**Parameters**

- `pin {Integer}` a number to identify the port (D2-D8) from which to do the reading
- `module_type {Integer}` a number to identify the model

    - `0` for [DHT11](http://wiki.seeedstudio.com/Grove-TemperatureAndHumidity_Sensor/)
    - `1` for [DHT22](http://wiki.seeedstudio.com/Grove-Temperature_and_Humidity_Sensor_Pro/)
    - `2` for DHT21
    - `3` for AM2301

**Returns**: a `{(Float, Float}` list where the 1st parameter is the temperature in ºC and the 2nd one is the humidity as a percentage.

**On Error**: it returns a `{(Float, Float)}` list containing `NaN`s. This happens when the sensor can't keep up with the demanded sample rate.

---

##`grovepi.ir_read_signal()`
Get the decoded value from the [Grove IR Receiver](https://www.seeedstudio.com/Grove-Infrared-Receiver-p-994.html). For this you need to use a remote control of any kind. The preferred one we use is the [Infrared Remote](https://www.dexterindustries.com/shop/infrared-remote/).

In order to use this function, you first need to call [grovepi.ir_recv_pin](#grovepiir_recv_pinpin) function to bind the functionality to a given port.

**Parameters**: None

**Returns**: a 3-element list of this form `{(Integer, Integer, Integer)}`

- The 1st element keeps an `{Integer}` corresponding to a certain brand:

    - `-1` for unknown and `0` for unused
    - RC2, RC5, NEC, SONY, PANASONIC, JVC, SAMSUNG, WHYNTER, AIWA_RC_T501, LG, SANYO, MITSUBISHI, DISH, SHARP, DENON, PRONTO, LEGO_PF having values from `1` to `17`

- The 2nd element is a 16-bit address used by some Panasonic and Sharp remotes
- The 3rd element is the 32-bit decoded value that can be used to identify which buttons were pressed - since there's no map for them you need to do it on a case-by-case basis

---

##`grovepi.ir_recv_pin(pin)`
Enable the [Grove IR Receiver](https://www.seeedstudio.com/Grove-Infrared-Receiver-p-994.html) on a given port. Used in conjunction with [grovepi.ir_read_signal](#grovepiir_read_signal) and [grovepi.ir_is_data](#grovepiir_is_data).

**Parameters**

- `pin {Integer}` The port (D2-D8) to which the IR receiver gets connected to

**Returns**: None

---

##`grovepi.ir_is_data()`
Checks if there's available data coming from the [Grove IR Receiver](https://www.seeedstudio.com/Grove-Infrared-Receiver-p-994.html). Used in conjunction with [grovepi.ir_read_signal](#grovepiir_read_signal) function.

**Parameters**: None

**Returns**: `True` or `False`

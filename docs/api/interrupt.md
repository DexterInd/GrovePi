#API - Interrupt-Based Devices

In this section the Python API reference for interrupt-based devices is described. This library is supported on both major versions
of Python: 2.x and 3.x.

The API for the following sensors is described in this section:

- [Grove Dust Sensor](https://www.seeedstudio.com/Grove-Dust-Sensor%EF%BC%88PPD42NS%EF%BC%89-p-1050.html)
- [Grove Encoder](https://www.seeedstudio.com/Grove-Encoder-p-1352.html)
- [Grove Water Flow Sensor](https://www.seeedstudio.com/M11%2A1.25-Water-Flow-Sensor-p-1345.html) of whose functionality can be used in other applications too

##`grovepi.dust_sensor_en(pin = 2)`
Enables the [Grove Dust Sensor](https://www.seeedstudio.com/Grove-Dust-Sensor%EF%BC%88PPD42NS%EF%BC%89-p-1050.html).

Cannot call this function if [grovepi.encoder_en](#grovepiencoder_en) or [grovepi.flowEnable](#grovepiflowenablepin-2) have been previously called. You first must disable them by using their appropriate function calls.

**Parameters**

- `pin {Integer}` the port (D2 or D3) to which the dust sensor is assigned to

**Returns**: None

---

##`grovepi.dust_sensor_dis()`
Disables the [Grove Dust Sensor](https://www.seeedstudio.com/Grove-Dust-Sensor%EF%BC%88PPD42NS%EF%BC%89-p-1050.html).

Required if you want to enable other sensors. It's generally a good practice to disable it after you're done with it.

**Parameters**: None

**Returns**: None

---

##`grovepi.dust_sensor_read()`
Reads the low pulse occupancy of the [Grove Dust Sensor](https://www.seeedstudio.com/Grove-Dust-Sensor%EF%BC%88PPD42NS%EF%BC%89-p-1050.html) in the given time period specified by [grovepi.get_dust_sensor_interval](#grovepiget_dust_sensor_interval).

**Parameters**: None

**Returns**: `{(Integer, Integer)}` list - the 1st element is `1` if the read value is a new one or `0` if it's old and the 2nd element holds the actual LPO (low pulse occupancy) time.

---

##`grovepi.dust_sensor_read_more()`
Returns more information than [grovepi.dust_sensor_read](#grovepidust_sensor_read) from the [Grove Dust Sensor](https://www.seeedstudio.com/Grove-Dust-Sensor%EF%BC%88PPD42NS%EF%BC%89-p-1050.html) in the given time period specified by [grovepi.get_dust_sensor_interval](#grovepiget_dust_sensor_interval).

**Parameters**: None

**Returns**: `{(Integer, Integer, Integer)}` list

- 1st element is the LPO time
- the 2nd one is the percentage (LPO time divided by total period)
- the 3rd is the concentration as measured in _pcs/283ml=0.01cf_ where the particle size is over _1um_

---

##`grovepi.get_dust_sensor_interval()`
Retrieves the [Grove Dust Sensor's](https://www.seeedstudio.com/Grove-Dust-Sensor%EF%BC%88PPD42NS%EF%BC%89-p-1050.html) period of time. By default, it's set to 30,000 ms (30 seconds) and on every power-up of the GrovePi, the interval needs to be reset if you want a different period other than the default one.

**Parameters**: None

**Returns**: The time the dust sensor collects data before it gets analyzed and sent back to the Raspberry Pi

---


##`grovepi.set_dust_sensor_interval(interval_ms)`
Set the [Grove Dust Sensor's](https://www.seeedstudio.com/Grove-Dust-Sensor%EF%BC%88PPD42NS%EF%BC%89-p-1050.html) period of time. By default, it's set to 30,000 ms (30 seconds).

**Parameters**

- `interval_ms {Integer}` the period in milliseconds of the dust sensor

**Returns**: None

---

##`grovepi.encoder_en()`
Enable the [Grove Encoder](https://www.seeedstudio.com/Grove-Encoder-p-1352.html) on port D2.

Bear in mind, this function must not be called if there's a device (dust sensor or flow meter) already assigned to port D2 - you must first disable them and then run this function.

**Parameters**: None

**Returns**: None

---

##`grovepi.encoder_dis()`
Disable the [Grove Encoder](https://www.seeedstudio.com/Grove-Encoder-p-1352.html) which sits on port D2.

The call to this function is required if you already have the encoder enabled and you want to either use a dust sensor or a flow meter on port D2.

**Parameters**: None

**Returns**: None

---

##`grovepi.encoderRead()`
Read the data off of the [Grove Encoder](https://www.seeedstudio.com/Grove-Encoder-p-1352.html) on port D2.

**Parameters**: None

**Returns**: `{(Integer, Integer)}` the 1st element is set to `1` if there's a value, `0` otherwise and the 2nd element represents the position of the encoder on a scale of 24 values (`1` to `24`). `-1`s are returned if there had been an error on reading.

---

##`grovepi.flowEnable(pin = 2)`
Enables the [Grove Water Flow Sensor](https://www.seeedstudio.com/M11%2A1.25-Water-Flow-Sensor-p-1345.html).

Cannot call this function if [grovepi.encoder_en](#grovepiencoder_en) or [grovepi.dust_sensor_en](#grovepidust_sensor_enpin-2) have been previously called. You first must disable them by using their appropriate function calls.

This functionality can also be used for counting the number of rising pulses in the given time period of 2,000 ms (2 seconds).

**Parameters**

- `pin {Integer}` the port (D2 or D3) to which the dust sensor is assigned to

**Returns**: None

---

##`grovepi.flowDisable()`
Disables the [Grove Water Flow Sensor](https://www.seeedstudio.com/M11%2A1.25-Water-Flow-Sensor-p-1345.html).

The call to this function is required if you already have the flow sensor enabled and you want to either use a dust sensor or an encoder on port D2.

**Parameters**: None

**Returns**: None

---

##`grovepi.flowRead()`
Enables the [Grove Water Flow Sensor](https://www.seeedstudio.com/M11%2A1.25-Water-Flow-Sensor-p-1345.html).


This functionality can also be used for counting the number of rising pulses in the given time period of 2,000 ms (2 seconds).

**Parameters**: None

**Returns**: the 1st element of the list is either `1` (for having received a new value) or `0` (or otherwise) and the 2nd element of it represents the number of pulse rises per 2,000ms cycle (2 seconds). `-1`s are returned if there's an error processing the request.

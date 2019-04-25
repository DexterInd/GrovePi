#API - Interrupt-Based Devices

In this section the Python API reference for interrupt-based devices is described. This library is supported on both major versions
of Python: 2.x and 3.x.

The API for the following sensors is described in this section:

- [Grove Dust Sensor](https://www.seeedstudio.com/Grove-Dust-Sensor%EF%BC%88PPD42NS%EF%BC%89-p-1050.html)
- [Grove Encoder](https://www.seeedstudio.com/Grove-Encoder-p-1352.html)
- [Grove Water Flow Sensor](https://www.seeedstudio.com/M11%2A1.25-Water-Flow-Sensor-p-1345.html) of whose functionality can be used in other applications too

---
**IMPORTANT**

This library and the other ones too are not thread-safe. You cannot call the GrovePi from multiple threads or processes
as that will put the GrovePi into a broken state.

In case you need to reset the GrovePi from your Raspberry Pi, [check this section](../fw/#resetting-the-grovepi).

---

##`grovepi.set_pin_interrupt()`
Attach an interrupt event to a port.

Can be used to count pulses, duration of pulses, set different kinds of trigger modes (on change, rising or falling edges) all done within a given period of time.

If there are subsequent calls to this set function without detaching the interrupt event first from a given pin, then it will overwrite the old setting and update it to reflect the latest one.

**Parameters**

- `pin {Integer}` can be pins D2-D8 to which the device is connected to
- `ftype {Integer}` the type of event/operation associated for the given pin. Can take values `grovepi.COUNT_CHANGES` (for counting the number of triggers) or `grovepi.COUNT_LOW_DURATION` (which measures how much time the signal stays low in a given period).
- `interrupt_mode {Integer}` triggering mode of the interrupt. It can be `grovepi.CHANGE`, `grovepi.FALLING` or `grovepi.RISING`, just like on the Arduino.
- `period {Integer}` specifying after how long the recorded value should be stored on the GrovePi to be subsequently read on the master device (Raspberry Pi). Measured in milliseconds. Minimum value shouldn't be too small (say under _5ms_) and the maximum value is _65535ms_.

**Returns**: None

---

##`grovepi.unset_pin_interrupt()`
Detach an interrupt event from a given pin.

**Parameters**

- `pin {Integer}` pins D2-D8 from which the interrupt is released from

**Returns**: None

---

##`grovepi.unset_all_interrupts()`
Detach all active interrupt events on all pins.

**Parameters**: None

**Returns**: None

---

##`grovepi.is_interrupt_active()`
Check if a pin has an interrupt event associated.

**Parameters**

- `pin {Integer}` pin to check if there's an associated interrupt event

**Returns**: `{Bool}` - `True` if it has an interrupt event associated and `False` if otherwise.

---

##`grovepi.get_active_interrupts()`
Get a list of all pins that have associated interrupt events.

**Parameters**: None

**Returns**: A list of integers representing the active pins that have interrupt events.

---

##`grovepi.read_interrupt_state()`
Get the recorded value by the interrupt event on the given pin.

If an interrupt is set on pin D2 with operation type set to `grovepi.COUNT_CHANGES` and mode of interrupt set to `grovepi.RISING` with a period set to 1000ms, then say if 567 rising edges are detected, then at the end of this period of 1000ms, this function will return for pin D2 value 567. And the returned value of this function on D2 pin will update every 1000ms, because that's the period that has been set for it. And the outcome varies depending on how the interrupt event is initially set.

**Parameters**

- `pin {Integer}` pin to check the recorded value for the previously associated interrupt event.

**Returns**: `{Bool}` - `True` if it has an interrupt event associated and `False` if otherwise.

---

##`grovepi.dust_sensor_en(pin = 2)`
Enables the [Grove Dust Sensor](https://www.seeedstudio.com/Grove-Dust-Sensor%EF%BC%88PPD42NS%EF%BC%89-p-1050.html).

Cannot call this function if [grovepi.encoder_en](#grovepiencoder_en) or [grovepi.flowEnable](#grovepiflowenablepin-2) have been previously called. You first must disable them by using their appropriate function calls.

**Parameters**

- `pin {Integer}` the pin (D2 or D3) to which the dust sensor is assigned to

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
Enable the [Grove Encoder](https://www.seeedstudio.com/Grove-Encoder-p-1352.html) on pin D2.

Bear in mind, this function must not be called if there's a device (dust sensor or flow meter) already assigned to pin D2 - you must first disable them and then run this function.

**Parameters**: None

**Returns**: None

---

##`grovepi.encoder_dis()`
Disable the [Grove Encoder](https://www.seeedstudio.com/Grove-Encoder-p-1352.html) which sits on pin D2.

The call to this function is required if you already have the encoder enabled and you want to either use a dust sensor or a flow meter on pin D2.

**Parameters**: None

**Returns**: None

---

##`grovepi.encoderRead()`
Read the data off of the [Grove Encoder](https://www.seeedstudio.com/Grove-Encoder-p-1352.html) on pin D2.

**Parameters**: None

**Returns**: `{(Integer, Integer)}` the 1st element is set to `1` if there's a value, `0` otherwise and the 2nd element represents the position of the encoder on a scale of 24 values (`1` to `24`). `-1`s are returned if there had been an error on reading.

---

##`grovepi.flowEnable(pin = 2)`
Enables the [Grove Water Flow Sensor](https://www.seeedstudio.com/M11%2A1.25-Water-Flow-Sensor-p-1345.html).

Cannot call this function if [grovepi.encoder_en](#grovepiencoder_en) or [grovepi.dust_sensor_en](#grovepidust_sensor_enpin-2) have been previously called. You first must disable them by using their appropriate function calls.

This functionality can also be used for counting the number of rising pulses in the given time period of 2,000 ms (2 seconds).

**Parameters**

- `pin {Integer}` the pin (D2 or D3) to which the dust sensor is assigned to

**Returns**: None

---

##`grovepi.flowDisable()`
Disables the [Grove Water Flow Sensor](https://www.seeedstudio.com/M11%2A1.25-Water-Flow-Sensor-p-1345.html).

The call to this function is required if you already have the flow sensor enabled and you want to either use a dust sensor or an encoder on pin D2.

**Parameters**: None

**Returns**: None

---

##`grovepi.flowRead()`
Enables the [Grove Water Flow Sensor](https://www.seeedstudio.com/M11%2A1.25-Water-Flow-Sensor-p-1345.html).


This functionality can also be used for counting the number of rising pulses in the given time period of 2,000 ms (2 seconds).

**Parameters**: None

**Returns**: the 1st element of the list is either `1` (for having received a new value) or `0` (or otherwise) and the 2nd element of it represents the number of pulse rises per 2,000ms cycle (2 seconds). `-1`s are returned if there's an error processing the request.

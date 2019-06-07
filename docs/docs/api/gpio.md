#API - GPIO Functions

In this section the Python API reference for GPIO functions is described. This library is supported on both major versions
of Python: 2.x and 3.x.

---
**IMPORTANT**

This library and the other ones too are not thread-safe. You cannot call the GrovePi from multiple threads or processes
as that will put the GrovePi into a broken state.

In case you need to reset the GrovePi from your Raspberry Pi, [check this section](../fw/#resetting-the-grovepi).

The functions don't verify if the input parameters are valid and therefore the parameters have to be verified/validated before that.
Calling a function with improper parameters can result in an undefined behavior for the GrovePi.
---

##`grovepi.digitalRead(pin)`
Reads whether a port's input is set high or low on the GrovePi.

**Parameters**

- `pin {Integer}` a number to identify the port (D2-D8) from which to do the reading

**Returns**: `0` or `1` depending on the input value

---

##`grovepi.digitalWrite(pin, value)`
Sets the output value to either `0` or `1` to a digital port on the GrovePi.

**Parameters**

- `pin {Integer}` a number to identify the port (D2-D8) to which to do the writing
- `value {Integer}` either `0` for 0 volts or `1` for maximum output voltage (usually 5 volts)

**Returns**: `1` all the time

---

##`grovepi.analogRead(pin)`
Detect an input voltage as a value from a given port on the GrovePi.

**Parameters**

- `pin {Integer}` a number to identify the port (A0-A2) from which to do the reading

**Returns**: a 10-bit `{Integer}` number that maps to the input voltage on the port

---

##`grovepi.analogWrite(pin, value)`
Set an output voltage on a PWM-enabled port by mapping the value to the desired voltage on the GrovePi.

**Parameters**

- `pin {Integer}` a number to identify the port (ports 3, 5, 6, 9) to which to do the writing
- `value {Integer}` an 8-bit number that maps from 0V to the referenced voltage of the GrovePi (5V)

**Returns**: `1` all the time

---

##`grovepi.pinMode(pin, mode)`
Sets a port to be either an OUTPUT or an INPUT port on the GrovePi.

**Parameters**

- `pin {Integer}` a number to identify the port (D2-D8) to which to do the change
- `mode {String}` `"OUTPUT"` for writing values or `"INPUT"` for reading

**Returns**: `1` all the time

#API - Complex Devices

In this section the Python API reference for more complex devices is described. This library is supported on both major versions
of Python: 2.x and 3.x.

The API for the following sensors is described in this section:

- [Grove LED bar](http://wiki.seeedstudio.com/Grove-LED_Bar/)
- [Grove 4-Digit Display](http://wiki.seeedstudio.com/Grove-4-Digit_Display/)
- [Grove Chainable RGB LED](https://www.seeedstudio.com/Grove-Chainable-RGB-LED-p-850.html)

---
**IMPORTANT**

This library and the other ones too are not thread-safe. You cannot call the GrovePi from multiple threads or processes
as that will put the GrovePi into a broken state.

In case you need to reset the GrovePi from your Raspberry Pi, [check this section](../fw/#resetting-the-grovepi).

The functions don't verify if the input parameters are valid and therefore the parameters have to be verified/validated before that.
Calling a function with improper parameters can result in an undefined behavior for the GrovePi.
---

##`grovepi.ledBar_init(pin, orientation)`
Initialize an [LED bar](http://wiki.seeedstudio.com/Grove-LED_Bar/).

**Parameters**

- `pin {Integer}` a number to identify the port (D2-D8) to which the LED bar is assigned to
- `orientation {Integer}` `0` to go from red to green or 1 to go the other way

**Returns**: `1` all the time

---

##`grovepi.ledBar_orientation(pin, orientation)`
Set the orientation on an already initialized [LED bar](http://wiki.seeedstudio.com/Grove-LED_Bar/).

**Parameters**

- `pin {Integer}` a number to identify the port (D2-D8) to which the LED bar is assigned to
- `orientation {Integer}` `0` to go from red to green or 1 to go the other way

**Returns**: `1` all the time

---

##`grovepi.ledBar_setLevel(pin, level)`
Set the level on an [LED bar](http://wiki.seeedstudio.com/Grove-LED_Bar/).

**Parameters**

- `pin {Integer}` a number to identify the port (D2-D8) to which the LED bar is assigned to
- `orientation {Integer}` `0` to `10` corresponding to the number of levels that exist on the LED bar.

**Returns**: `1` all the time

---

##`grovepi.ledBar_toggleLed(pin, led)`
Toggle the state of one LED of the 10 levels of the [LED bar](http://wiki.seeedstudio.com/Grove-LED_Bar/).

**Parameters**

- `pin {Integer}` a number to identify the port (D2-D8) to which the LED bar is assigned to
- `led {Integer}` taking values from `0` to `10` depending on which LED to toggle

**Returns**: `1` all the time

---

##`grovepi.ledBar_setBits(pin, state)`
Set the LED activations of the [LED bar](http://wiki.seeedstudio.com/Grove-LED_Bar/) based on the binary representation of a 10-bit number.

**Parameters**

- `pin {Integer}` a number to identify the port (D2-D8) to which the LED bar is assigned to
- `state {Integer}` a number from `0` to `1023` that covers all states for all 10 LEDs of the LED bar

**Returns**: `1` all the time

---

##`grovepi.ledBar_getBits(pin)`
Read the state of LED activations on the [LED bar](http://wiki.seeedstudio.com/Grove-LED_Bar/).

**Parameters**

- `pin {Integer}` a number to identify the port (D2-D8) to which the LED bar is assigned to

**Returns**: a number from `0` to `1023` to represent the binary state of all 10 LEDs of the LED bar

---

##`grovepi.fourDigit_init(pin)`
Initialize a [Grove 4-Digit Display](http://wiki.seeedstudio.com/Grove-4-Digit_Display/).

**Parameters**

- `pin {Integer}` the port (D2-D8) to which the 4-Digit display is set to

**Returns**: `1` all the time

---

##`grovepi.fourDigit_number(pin, value, leading_zero)`
Set the [Grove 4-Digit Display](http://wiki.seeedstudio.com/Grove-4-Digit_Display/) to display a number.

**Parameters**

- `pin {Integer}` the port (D2-D8) to which the 4-Digit display is set to
- `value {Integer}` a value between `0` and `9999` representing the number to be printed on the display
- `leading_zero {Boolean}` whether to add leading zeros or not

**Returns**: `1` all the time

---

##`grovepi.fourDigit_brightness(pin, brightness)`
Set the brightness of the [Grove 4-Digit Display](http://wiki.seeedstudio.com/Grove-4-Digit_Display/).

**Parameters**

- `pin {Integer}` the port (D2-D8) to which the 4-Digit display is set to
- `brightness {Integer}` a number between `0` (for the darkest option) and `7` (for the brightest) representing the brightness of the display

**Returns**: `1` all the time

---

##`grovepi.fourDigit_digit(pin, segment, value)`
Set individual segment of the [Grove 4-Digit Display](http://wiki.seeedstudio.com/Grove-4-Digit_Display/).

**Parameters**

- `pin {Integer}` the port (D2-D8) to which the 4-Digit display is set to
- `segment {Integer}` a number from `0` to `3` representing the segment
- `value {Integer}` value of the segment - `0` to `15`

**Returns**: `1` all the time

---

##`grovepi.fourDigit_segment(pin, segment, leds)`
Set the individual LED segments of a digit of the [Grove 4-Digit Display](http://wiki.seeedstudio.com/Grove-4-Digit_Display/).

**Parameters**

- `pin {Integer}` the port (D2-D8) to which the 4-Digit display is set to
- `segment {Integer}` which segment of the display to modify (`0` to `3`)
- `leds {Integer}` a number from `0` to `255` representing the binary activations of the selected `segment` - the 8th bit is the colon

**Returns**: `1` all the time

---

##`grovepi.fourDigit_score(pin, left, right)`
Set values on either side of the [Grove 4-Digit Display](http://wiki.seeedstudio.com/Grove-4-Digit_Display/).
To the left and right values, leading zeros are added and the colon is lit up

**Parameters**

- `pin {Integer}` the port (D2-D8) to which the 4-Digit display is set to
- `left {Integer}` value to be displayed on the left side of the display (takes values from `0` to `99`)
- `right {Integer}` value to be displayed on the right side of the display (takes values from `0` to `99`)

**Returns**: `1` all the time

---

##`grovepi.fourDigit_monitor(pin, analog, duration)`
Display the [analogRead](#grovepianalogreadpin) values onto the [Grove 4-Digit Display](http://wiki.seeedstudio.com/Grove-4-Digit_Display/) for a given time.

**Parameters**

- `pin {Integer}` the port (D2-D8) to which the 4-Digit display is set to
- `analog {Integer}` the port (A0-A2) on which analog values are read from
- `duration {Integer}` for how many seconds (`0` to `255`) the readings are to be displayed

**Returns**: `1` all the time

---

##`grovepi.fourDigit_on(pin)`
Turn the whole [Grove 4-Digit Display](http://wiki.seeedstudio.com/Grove-4-Digit_Display/) on.

**Parameters**

- `pin {Integer}` the port (D2-D8) to which the 4-Digit display is set to

**Returns**: `1` all the time

---

##`grovepi.fourDigit_off(pin)`
Turn the whole [Grove 4-Digit Display](http://wiki.seeedstudio.com/Grove-4-Digit_Display/) off.

**Parameters**

- `pin {Integer}` the port (D2-D8) to which the 4-Digit display is set to

**Returns**: `1` all the time

---

##`grovepi.storeColor(red, green, blue)`
Store a color for later use with the [Grove Chainable RGB LED](https://www.seeedstudio.com/Grove-Chainable-RGB-LED-p-850.html).

**Parameters**

- `red {Integer}` value from `0` to `255`
- `green {Integer}` value from `0` to `255`
- `blue {Integer}` value from `0` to `255`

**Returns**: `1` all the time

---

##`grovepi.chainableRgbLed_init(pin, numLeds)`
Initialize a number of [chained LEDs](https://www.seeedstudio.com/Grove-Chainable-RGB-LED-p-850.html) on given port.

**Parameters**

- `pin {Integer}` the port (D2-D8) to which the Grove RGB LED(s) are connected to
- `numLeds {Integer}` number of chained LEDs

**Returns**: `1` all the time

---

##`grovepi.chainableRgbLed_test(pin, numLeds, testColor)`
Initialize [chained LEDs](https://www.seeedstudio.com/Grove-Chainable-RGB-LED-p-850.html) on given port and set a test color on all of them.

**Parameters**

- `pin {Integer}` the port (D2-D8) to which the Grove RGB LED(s) are connected to
- `numLeds {Integer}` number of chained LEDs
- `testColor {Integer}` the color to use for all chained LEDs

    - `0` for black (or nothing)
    - `1` for blue
    - `2` for green
    - `3` for cyan
    - `4` for red
    - `5` for magenta
    - `6` for yellow
    - `7` for white

**Returns**: `1` all the time

---

##`grovepi.chainableRgbLed_pattern(pin, pattern, whichLed)`
Set one or more [chained LEDs](https://www.seeedstudio.com/Grove-Chainable-RGB-LED-p-850.html) to a stored color following a given pattern.

**Parameters**

- `pin {Integer}` the port (D2-D8) to which the Grove RGB LED(s) are connected to
- `pattern {Integer}`

    - `0` for this LED only
    - `1` for all LEDs except this LED
    - `2` this LED and all LEDs inwards
    - `3` this LED and all LEDs outwards

- `whichLed {Integer}` the index of the LED you wish to set counting outwards from the GrovePi starting with `0`

**Returns**: `1` all the time

---

##`grovepi.chainableRgbLed_modulo(pin, offset, divisor)`
Set one or more [chained LEDs](https://www.seeedstudio.com/Grove-Chainable-RGB-LED-p-850.html) to a stored color following the "pattern" of the modulo operation.

**Parameters**

- `pin {Integer}` the port (D2-D8) to which the Grove RGB LED(s) are connected to
- `offset {Integer}` the index of the LED you want to start at (`0` is for the 1st LED)
- `divisor {Integer}` sets the color to those LEDs of whose indexes divided by `divisor` have the remainder set to `0` - for `divisor=1` every LED gets set, but for `divisor=2` every 2nd LED gets set  

**Returns**: `1` all the time

---

##`grovepi.chainableRgbLed_setLevel(pin, level, reverse)`
Set one or more [chained LEDs](https://www.seeedstudio.com/Grove-Chainable-RGB-LED-p-850.html) to a stored color similar to a bar graph.

**Parameters**

- `pin {Integer}` the port (D2-D8) to which the Grove RGB LED(s) are connected to
- `level {Integer}` the number of LEDs you want to set to the stored color
- `reverse {Integer}` `0` when counting outwards from the GrovePi or `1` when it's the other way (from the most outward LED inwards)

**Returns**: `1` all the time

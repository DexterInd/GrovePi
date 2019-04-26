## Flashing the Firmware

To flash the firmware, you must first have the GrovePi library/repository installed so for this you must follow the [Getting Started guide](quickstart.md#how-to-install).

Once the library is installed on the Raspberry Pi, run the following commands to have the firmware flashed onto the GrovePi:

```bash
cd ~/Dexter/GrovePi/Firmware
bash firmware_update.sh
```
This updates you to the latest version of the firmware which is the `1.4.0`.

---
**NOTE TO OTHER LIBRARIES**

Because the `1.3.0` firmware was recently released, lots of other libraries written in other languages other than Python are yet to be updated, so
they need to run on an older version of the firmware, specifically the `1.2.7`.

The `1.2.7` version can be found in `~/Dexter/GrovePi/Firmware/Archive` as `grove_pi_v1_2_7.cpp.hex`. If you need to run on this older version, follow these steps to burn the firmware:
```bash
mv ~/Dexter/GrovePi/Firmware/grove_pi_firmware.hex ~/Dexter/GrovePi/Firmware/grove_pi_v1_3_0.hex.bak
cp ~/Dexter/GrovePi/Firmware/Archive/grove_pi_v1_2_7.cpp.hex ~/Dexter/GrovePi/Firmware/grove_pi_firmware.hex
bash firmware_update.sh
```

---

## Running Tests

To run the entire suite of tests for the GrovePi follow these bash instructions:
```bash
cd ~/Dexter/GrovePi/Troubleshooting
sudo bash all_tests.sh
```

At the end of this process you'll get a `log.txt` file on your Desktop at `~/Desktop/log.txt`.

Also, to see with which version of the firmware the library installed on the Raspberry Pi works with you can go to `~/Dexter/GrovePi` directory and run:
```bash
python grovepi.py
```
This should output a version number (of the GrovePi's firmware). Older versions of the firmware (<=`v1.2.7`) won't get displayed when calling `python grovepi.py`.
```bash
pi@raspberrypi:~ $ python grovepi.py
library supports this fw versions: 1.4.0
```

To see which is the version of the current firmware loaded on the GrovePi you can either run the above test (`... all_test.sh`) from the `Troubleshooting/` directory or you can run these commands:
```python
import grovepi
print(grovepi.version())
```

There are also cases when the GrovePi doesn't respond to requests. In this situation, you would normally see an exception appearing in Python. More often than not, these can be the source of problems:

- A non-present firmware on the GrovePi.
- A mismatch of versions between the firmware and the library on the Raspberry Pi.

In both of these situations, re-flashing the firmware is all it's needed.

## Building the Firmware

There may be cases where additional modification to the firmware is required to accommodate someone's particular requirements. In this case,
building the firmware and then uploading it is crucial. During our production, we use [PlatformIO](https://platformio.org/) along with [Atom IDE](https://atom.io/).

Once you get them both installed on your machine, open Atom IDE and add as a project the `/Firmware/Source/grovepi` directory. The added directory will have the following structure:

- `lib/`
- `src/`
- `.gitignore`
- `.travis.yml`
- `extra_script.py`
- `platformio.ini`

Next, click on the build button or use **ALT-CTRL-B** key combination to build the firmware with PlatformIO. Once that it's done, head over to `/Firmware/Source/grovepi/.pioenvs/grovepi` directory and notice the `firmware.hex`. That's the firmware that was just built. You can then burn that to your GrovePi.

## Resetting the GrovePi

To reset the GrovePi from your Raspberry Pi, run the following command provided you have installed the GrovePi library on your image:
```bash
avrdude -c gpio -p m328p
```

<!-- ## Enabling Software I2C

The GrovePi and the Raspberry Pi communicate over an I2C connection, but the problem with the Raspberry Pi's HW implementation has to do with the clock stretching mechanism. This mechanism is badly implemented and can lead to corrupted transfers with the GrovePi.

More details on this issue can be found on these tickets: [raspberrypi/linux/issues/254](https://github.com/raspberrypi/linux/issues/254) and [dexterind/grovepi/issues/411](https://github.com/DexterInd/GrovePi/issues/411).

In order to avoid having problems caused by the clock-stretching mechanism, you can use our bit-bang implementation of the I2C that uses the [RPi.GPIO](https://pypi.org/project/RPi.GPIO/) library. In order to have this alternative software I2C used instead, install the [DI-Sensors library](http://di-sensors.readthedocs.io/en/master/quickstart.html#how-to-install-the-di-sensors).

To check which I2C you're using, you can import the `grovepi` module and then check the value of `grovepi.whichI2C` attribute. If it's set to `"periphery"` then it means the HW I2C is used and otherwise if it's set to `"software"` then it's using the DI-Sensors' one which is bit-banged. -->

## Flashing the Firmware

To flash the firmware, you must first have the GrovePi library/repository installed so for this you must follow the [Getting Started guide](quickstart.md#how-to-install).

Once the library is installed on the Raspberry Pi, run the following commands to have the firmware flashed onto the GrovePi:

```bash
cd ~/Dexter/GrovePi/Firmware
bash firmware_update.sh
```
This updates you to the latest version of the firmware which is the `1.3.0`.

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

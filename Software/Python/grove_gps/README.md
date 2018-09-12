## Using the [Grove GPS Module](http://www.seeedstudio.com/depot/Grove-GPS-p-959.html?cPath=25_130) with the GrovePi

### Setting It Up

On newer versions of the Raspberry Pi, the hardware serial port `/dev/ttyAMAO` which is used in our library, is actually set to be used by the bluetooth module, leaving the software implementation `/dev/ttyS0` (aka mini UART) to the actual pins of the serial line.
The problem with this mini UART is that it's too slow for what we need, so we have to switch them so that the hardware serial points to our serial pins.  

To do that, add/modify these lines to `/boot/config.txt`
```bash
dtoverlay=pi3-miniuart-bt
dtoverlay=pi3-disable-bt
enable_uart=1
```

Next, remove the 2 console statements from `/boot/cmdline.txt`.
Initially, `/boot/cmdline.txt` might look this way:
```
dwc_otg.lpm_enable=0 console=serial0,115200 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline fsck.repair=yes root wait
```
After you remove the 2 statements, it should be like this:
```
dwc_otg.lpm_enable=0 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline fsck.repair=yes root wait
```

Once you've done these 2 steps from above, a reboot will be required. Do it now, and then proceed to the next section.

For more information on how the serial ports are set up, you can [read this article](https://spellfoundry.com/2016/05/29/configuring-gpio-serial-port-raspbian-jessie-including-pi-3/#Disabling_the_Console).

### Running it

To run the GPS script, you need to have followed the instructions in the previous section and have connected the [Grove GPS Module](http://www.seeedstudio.com/depot/Grove-GPS-p-959.html?cPath=25_130) to the **RPIser** port of the GrovePi.

The script can be either launched with Python 2 or Python 3.
```bash
sudo python dextergps.py
```
or
```bash
sudo python3 dextergps.py
```

The output of any of these 2 commands looks this way:
```bash
['$GPGGA', '150954.000', '4520.7858', 'N', '02557.6659', 'E', '1', '5', '2.84', '76.9', 'M', '36.1', 'M', '', '*6E']
['$GPGGA', '150955.000', '4520.7859', 'N', '02557.6655', 'E', '1', '5', '2.84', '77.0', 'M', '36.1', 'M', '', '*6A']
['$GPGGA', '150956.000', '4520.7861', 'N', '02557.6652', 'E', '1', '5', '2.85', '77.0', 'M', '36.1', 'M', '', '*64']
['$GPGGA', '150957.000', '4520.7861', 'N', '02557.6645', 'E', '1', '4', '2.90', '77.1', 'M', '36.1', 'M', '', '*67']
['$GPGGA', '150958.000', '4520.7861', 'N', '02557.6645', 'E', '1', '4', '2.90', '77.1', 'M', '36.1', 'M', '', '*68']
['$GPGGA', '150959.000', '4520.7861', 'N', '02557.6645', 'E', '1', '4', '2.90', '77.1', 'M', '36.1', 'M', '', '*69']
['$GPGGA', '151000.000', '4520.7861', 'N', '02557.6645', 'E', '1', '4', '2.90', '77.1', 'M', '36.1', 'M', '', '*6D']
['$GPGGA', '151001.000', '4520.7861', 'N', '02557.6645', 'E', '1', '4', '2.90', '77.1', 'M', '36.1', 'M', '', '*6C']
['$GPGGA', '151002.000', '4520.7863', 'N', '02557.6618', 'E', '1', '4', '2.90', '77.5', 'M', '36.1', 'M', '', '*61']
['$GPGGA', '151003.000', '4520.7864', 'N', '02557.6612', 'E', '1', '4', '2.90', '77.6', 'M', '36.1', 'M', '', '*6E']
['$GPGGA', '151004.000', '4520.7865', 'N', '02557.6606', 'E', '1', '4', '2.90', '77.6', 'M', '36.1', 'M', '', '*6D']
['$GPGGA', '151005.000', '4520.7865', 'N', '02557.6597', 'E', '1', '4', '2.90', '77.6', 'M', '36.1', 'M', '', '*67']
['$GPGGA', '151006.000', '4520.7865', 'N', '02557.6588', 'E', '1', '4', '2.90', '77.6', 'M', '36.1', 'M', '', '*6A']
```

### Regarding the Library

**gps.lat** and **gps.NS** go hand in hand, so do **gps.lon** and **gps.EW**

**gps.latitude** and **gps.longitude** are calculated to give you a Google Map appropriate format and make use of negative numbers to indicate either South or West

*Note*:
You would only get good data when fix is 1 and you have 3 or more satellites in view. You might have to take the module near a window with access to open sky for good results

### Old GPS Scripts

`dextergps.py` is the new go-to script for getting values off of the Grove GPS module. The old ones that are no longer used but are kept in here for legacy reasons are:

* [grove_gps_data.py](grove_gps_data.py)
* [grove_gps_hardware_test.py](grove_gps_hardware_test.py)
* [GroveGPS.py](GroveGPS.py)

#!/usr/bin/env bash
#Adapted from tutorial here: http://www.linuxcircle.com/2015/05/03/how-to-install-smbus-i2c-module-for-python-3/



apt-get install python3-dev libi2c-dev
cd i2c-tools-3.1.0/py-smbus
python3 setup.py build
python3 setup.py install

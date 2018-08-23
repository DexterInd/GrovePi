#!/usr/bin/python #!/usr/bin/env python
#
# GrovePi Python Setup
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

try:
	with open('package_description.rst', 'r') as file_description:
		description = file_description.read()

except IOError:
	description = "Check more on https://pypi.python.org/pypi/grovepi"

package_dirs_list = {
	'dextergps' : 'grove_gps/',
	'lsm303d' : 'grove_6axis_acc_compass/',
	'adxl345' : 'grove_accelerometer_16g/',
	'grove_barometer_lib' : 'grove_barometer_sensors/barometric_sensor_bmp085'
}

# To install the GrovePi library systemwide, use: sudo python setup.py install
import setuptools
setuptools.setup(
    name = "grovepi",
    version = "1.0.0",

    description = "Drivers for using the GrovePi+ in Python",
    long_description = description,

    author = "Dexter Industries",
    author_email = "contact@dexterindustries.com",

    license = 'MIT',
    classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'License :: OSI Approved :: MIT License',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Embedded Systems',
    'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    url = "https://github.com/DexterInd/GrovePi",

    keywords = ['robot', 'grovepi', 'grovepi+', 'dexter industries', 'learning', 'education', 'iot', 'internet of things', 'prototyping'],

	# packages = [
	# 	'dextergps',
	# 	# 'lsm303d',
	# 	# 'adxl345',
	# 	# 'grove_barometer_lib'
	# ],
	# package_dir = {
	# 	'dextergps' : 'grove_gps/',
	# 	# 'lsm303d' : 'grove_6axis_acc_compass/',
	# 	# 'adxl345' : 'grove_accelerometer_16g/',
	# 	# 'grove_barometer_lib' : 'grove_barometer_sensors/barometric_sensor_bmp085'
	# },
    py_modules = ['grovepi', 'grove_gps/dextergps'],
    install_requires = ['numpy', 'smbus-cffi', 'RPi.GPIO', 'serial'],
	test_suite = 'test_suite.TestMethods'
)

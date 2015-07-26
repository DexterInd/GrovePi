#!/usr/bin/python #!/usr/bin/env python
#
# GrovePi Python Setup
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
'''
## License
 GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
 Copyright (C) 2015  Dexter Industries

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.
'''
# To install the GrovePi library systemwide, use: sudo python setup.py install
import setuptools
setuptools.setup(
	name="grovepi",
	description="Drivers and examples for using the GrovePi in Python",
	author="Dexter Industries",
	url="http://www.dexterindustries.com/GrovePi/",
	py_modules=['grovepi'],
	#install_requires=open('requirements.txt').readlines(),
)

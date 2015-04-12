#!/usr/bin/python #!/usr/bin/env python
#
# GrovePi Python Setup
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# LICENSE: 
# These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.
#
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

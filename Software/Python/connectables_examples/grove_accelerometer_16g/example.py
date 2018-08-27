# ADXL345 Python example 
#
# author:  Jonathan Williamson
# license: BSD, see LICENSE.txt included in this package
# 
# This is an example to show you how to the Grove +-16g Accelerometer
# http://www.seeedstudio.com/depot/Grove-3Axis-Digital-Accelerometer16g-p-1156.html

from adxl345 import ADXL345
  
adxl345 = ADXL345()
    
axes = adxl345.getAxes(True)
print("ADXL345 on address 0x%x:" % (adxl345.address))
print("   x = %.3fG" % ( axes['x'] ))
print("   y = %.3fG" % ( axes['y'] ))
print("   z = %.3fG" % ( axes['z'] ))

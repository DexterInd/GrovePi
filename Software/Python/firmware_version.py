import grovepi

try:
    print "GrovePi has firmware version:", grovepi.version()

except KeyboardInterrupt:
    print "KeyboardInterrupt"
except IOError:
    print "Error"

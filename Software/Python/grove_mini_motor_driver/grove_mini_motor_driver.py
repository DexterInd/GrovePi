from sys import platform
import datetime

# Library written for Python 3!

left_channel = 0x60
right_channel = 0x62

# function for returning a SMBus object
# checks the Rpi version before it selects the bus
def getNewSMBus():
    bus = None

    if platform == 'uwp':
        import winrt_smbus as smbus
        bus = smbus.SMBus(1)
    else:
        import smbus
        import RPi.GPIO as GPIO
        revision = GPIO.RPI_REVISION

        if revision == 2 or revision == 3:
            bus = smbus.SMBus(1)
        else:
            bus = smbus.SMBus(0)
    return bus

# function for returning a formatted time date
def getTime():
    return datetime.datetime.now().strftime("%m-%b-%Y %H:%M:%S.%f")

# function for mapping a value which goes from
# left_min to left_max to right_min & right_max
def translateValues(value, left_min, left_max, right_min, right_max):
    # figure out how 'wide' each range is
    left_span = left_max - left_min
    right_span = right_max - right_min

    # convert the left range into a 0-1 range (float)
    value_scaled = float(value - left_min) / float(left_span)

    # convert the 0-1 range into a value in the right range.
    return right_min + (value_scaled * right_span)

# class for the DRV8830 driver
# the Grove Mini Motor driver is made of 2 DRV8830 drivers
# each of it controlling a motor channel
# the driver communicates via I2C
class DRV8830:
    # the constructor takes an I2C address and an optional SMBus object
    # if the SMBus object is not provided, it will create one on its own
    def __init__(self, channel_address, _bus = None):
        self.address = channel_address

        if _bus is None:
            self.bus = getNewSMBus()
        else:
            self.bus = _bus

        # fault register address and bit positions for each fault condition
        self.FAULT_REG = 0x01
        self.CLEAR = 0x80
        self.ILIMIT = 0x10
        self.OTS = 0x08
        self.UVLO = 0x04
        self.OCP = 0x02
        self.FAULT = 0x01

        # control register address and byte commands for it
        self.CONTROL_REG = 0x00
        self.STANDBY = 0x00
        self.REVERSE = 0x01
        self.FORWARD = 0x02
        self.BRAKE = 0x03

        # minimum speed in hexa
        self.MIN_SPEED = 0x06
        # maximum speed in hexa
        self.MAX_SPEED = 0x3F

        # dictionary for the fault register
        self.FAULT_TABLE = {
        self.ILIMIT : 'extended current limit event',
        self.OTS : 'overtemperature condition',
        self.UVLO : 'undervoltage lockout',
        self.OCP : 'overcurrent event',
        self.FAULT : 'unknown condition'
        }
        self.FAULT_TABLE_KEYS = list(self.FAULT_TABLE.keys())

    # function for actuating the motor on the given address
    # state might be = {STANDBY, REVERSE, FORWARD, BRAKE}
    # percentage_speed can be = 0 -> 100 (represents the percentage of the maximum available thrust)
    def motorWrite(self, state, percentage_speed = 0):
        calculated_speed = int(translateValues(percentage_speed, 0, 100, self.MIN_SPEED, self.MAX_SPEED))
        register_value = (calculated_speed << 2) + state

        self.bus.write_byte_data(self.address, self.CONTROL_REG, register_value)
        fault_strings = self.__readFaults()
        self.bus.write_byte_data(self.address, self.FAULT_REG, self.CLEAR)

        # in case we detect a fault
        # raise a RuntimeWarning with the detailed information
        if not fault_strings is None:
            result = "; ".join(fault_strings)
            raise RuntimeWarning(result)

    # private function for reading fault reports from the DRV8830 driver
    # returns a list of strings and each of the strings is about an encountered fault
    def __readFaults(self):
        faults_data = self.bus.read_byte_data(self.address, self.FAULT_REG)
        string = None

        for fault_key in self.FAULT_TABLE_KEYS:
            if faults_data & fault_key > 0:
                if string is None:
                    string = []
                string.append(self.FAULT_TABLE[fault_key])

        return string

    # whenever the object is freed, we shutdown the motors
    # if the motors aren't shut down, then they will continue to work/spin
    # even if you "reboot" the motor driver
    def __del__(self):
        self.motorWrite(self.STANDBY)

# class for managing the 2 DRV8830 drivers the Grove Mini Motor Driver has
class MiniMotorDriver:
    # obviously, we need the two I2C addresses of the DRV8830 drivers
    # the 2 addresses are: 0x60 & 0x62
    def __init__(self, ch1, ch2, _bus = None):
        if _bus is None:
            self.bus = getNewSMBus()
        else:
            self.bus = _bus

        self.left_motor = DRV8830(ch1)
        self.right_motor = DRV8830(ch2)
        self.display_faults = False

        # variables for the implementation I'm bringing on 24th of April
        #self.wheel_track = 0.01
        #self.wheel_diameter = 0.05
        #self.max_wheel_rpm = 1.2

    # private function for printing in a nicely formatted way the strings
    def __print(self, *strings):
        message_string = ""
        for string in strings:
            message_string += "[" + string + "]"

        print(message_string)

    # enable / disable displaying driver operations / statuses / warnings
    def setDisplayFaults(self, choice = True):
        self.display_faults = choice

    # private function which is centered on raising exceptions
    # you don't need to care about it
    # leave it to the pro: haha!
    def __writeMotor(self, motor, state, fail_description, speed = 0):
        try:
            motor.motorWrite(state, speed)

        except RuntimeWarning as message:
            if self.display_faults:
                self.__print(getTime(), fail_description, str(message))

    # command the 2 motors to go forward
    # speed = 0-100 %
    def moveForward(self, speed):
        self.__print(getTime(), "forward", "speed = " + str(speed) + "%")

        self.__writeMotor(self.left_motor, self.left_motor.FORWARD, "left motor warning", speed)
        self.__writeMotor(self.right_motor, self.right_motor.FORWARD, "right motor warning", speed)

    # command the 2 motors to go backwards
    # speed = 0-100%
    def moveBackwards(self, speed):
        self.__print(getTime(), "reverse", "speed = " + str(speed) + "%")

        self.__writeMotor(self.left_motor, self.left_motor.REVERSE, "left motor warning", speed)
        self.__writeMotor(self.right_motor, self.right_motor.REVERSE, "right motor warning", speed)

    # command the left motor to go in one of the set directions at a certain speed
    # direction = {'FORWARD', 'REVERSE'}
    # speed = 0-100%
    def setLeftMotor(self, direction, speed):
        if direction == "FORWARD":
            self.__print(getTime(), "left motor", "speed = " + str(speed) + "%")
            self.__writeMotor(self.left_motor, self.left_motor.FORWARD, "left motor warning", speed)

        elif direction == "REVERSE":
            self.__print(getTime(), "left motor", "speed = " + str(speed) + "%")
            self.__writeMotor(self.left_motor, self.left_motor.REVERSE, "left motor warning", speed)

    # command the right motor to go in one of the set directions at a certain speed
    # direction = {'FORWARD', 'REVERSE'}
    # speed = 0-100%
    def setRightMotor(self, direction, speed):
        if direction == "FORWARD":
            self.__print(getTime(), "right motor", "speed = " + str(speed) + "%")
            self.__writeMotor(self.right_motor, self.right_motor.FORWARD, "right motor warning", speed)

        elif direction == "REVERSE":
            self.__print(getTime(), "right motor", "speed = " + str(speed) + "%")
            self.__writeMotor(self.right_motor, self.right_motor.REVERSE, "right motor warning", speed)

    # command which forces the left motor to stop ASAP
    # it uses counter acts with an electromotive force in order to stop the motor from spinning faster
    # might raise some warnings depending on how good the power supply is
    def stopLeftMotor(self):
        self.__print(getTime(), "left motor", "stop")
        self.__writeMotor(self.left_motor, self.left_motor.BRAKE, "left motor warning")

    # command which forces the right motor to stop ASAP
    # it uses counter acts with an electromotive force in order to stop the motor from spinning faster
    # might raise some warnings depending on how good the power supply is
    def stopRightMotor(self):
        self.__print(getTime(), "right motor", "stop")
        self.__writeMotor(self.right_motor, self.right_motor.BRAKE, "right motor warning")

    # command which forces both the motor to stop ASAP
    # it uses counter acts with an electromotive force in order to stop the motors from spinning faster
    # might raise some warnings depending on how good the power supply is
    def stopMotors(self):
        self.stopLeftMotor()
        self.stopRightMotor()

    # command which kills the power to the motors
    def disableMotors(self):
        self.__print(getTime(), "standby motors")

        self.__writeMotor(self.left_motor, self.left_motor.STANDBY, "left motor warning")
        self.__writeMotor(self.right_motor, self.right_motor.STANDBY, "right motor warning")

"""
Will be implemented on Monday

    def setWheelTrack(self, centimeters):
        self.wheel_track = centimeters / 100

    def setWheelDiameter(self, centimeters):
        self.wheel_diameter = centimeters / 100

    def setWheelMaxRPM(self, RPM):
        self.max_wheel_rpm = RPM

    def bangLeft(self, degrees, direction, speed):
        # code
        #

    def bangRight(self, degrees, direction,speed):
        # code
        #

    def rotateOnTheSpot(self, degrees, orientation):
        # code
        #
"""

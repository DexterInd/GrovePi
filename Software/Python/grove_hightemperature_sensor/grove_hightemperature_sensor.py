import grovepi
import math

# Library written for Python 3!

# take a look in the datasheet
# http://www.mouser.com/catalog/specsheets/Seeed_111020002.pdf

# class for the K-Type temperature sensor (w/ long probe/sonde)
class HighTemperatureSensor:

    # initialize the object with the appropriate sensor pins on the GrovePi
    def __init__(self, _temperature_pin, _thermocouple_pin):
        # save the variables inside the object
        self.temperature_pin = _temperature_pin
        self.thermocouple_pin = _thermocouple_pin

        # save custom values taken from the datasheet
        # and keep them in private (so the general user can't access them)
        self.__vol_offset = 350.0
        self.__amp_av = 54.16

        # take a look at the datasheet
        self.__sensor_table = [
        [0, 2.5173462e1, -1.1662878, -1.0833638, -8.9773540/1e1, -3.7342377/1e1,
        -8.6632643/1e2, -1.0450598/1e2, -5.1920577/1e4],

        [0, 2.508355e1, 7.860106/1e2, -2.503131/1e1, 8.315270/1e2, -1.228034/1e2,
        9.804036/1e4, -4.413030/1e5, 1.057734/1e6, -1.052755/1e8],

        [-1.318058e2, 4.830222e1, -1.646031, 5.464731/1e2, -9.650715/1e4,
        8.802193/1e6, -3.110810/1e8]
        ]

        # set the pins as INPUT
        # this sensor outputs analog values so you can
        # use one of the 3 analog ports on the GrovePi
        grovepi.pinMode(self.temperature_pin, "INPUT")
        grovepi.pinMode(self.thermocouple_pin, "INPUT")

    # function for retrieving the room temperature_pin
    # if values exceed what's written in the datasheet
    # then it throws a ValueError exception
    def getRoomTemperature(self):
        # ratio for translating from 3.3V to 5.0V (what we read is in the range of 0 -> 3.3V)
        voltage_ratio = 5.0 / 3.3

        # and multiply what we read by that ratio
        # and read it for about 12 times -> this way we get smoother readings
        # the reason we average it is because the table we provided isn't big enough
        # and as a consequence you'd get values like (20 degrees, 24 degrees and so on)
        analog_sum = 0
        for step in range(12):
            analog_sum += grovepi.analogRead(self.temperature_pin)
        analog_value = (analog_sum / 12) * voltage_ratio
        # see the datasheet for more information
        calculated_resistance = (1023 - analog_value) * 10000 / analog_value
        calculated_temperature = 1 / (math.log(calculated_resistance / 10000) / 3975 + 1 / 298.15) - 273.15

        # if the values exceed a certain threshold
        # then raise a ValueError exception
        if not (calculated_temperature >= -50.0 and calculated_temperature <= 145.0):
            raise ValueError('temperature out of range')

        # and return what we got calculated
        return calculated_temperature

    # function for retrieving the temperature at the tip of the probe / sonde
    # only the temperature of the tip of the probe is measured
    # the rest of the K-Type sensor is for reaching the hot environment you want to measure
    # so you don't get burned
    def getTemperature(self):
        # read what we get on the 2 analog pins
        # the K-Type sensor is also called a Thermocouple sensor
        voltage = self.__getThermocoupleVoltage()
        room_temperature = self.getRoomTemperature()

        # calculate the thermocouple/probe/sonde temperature
        # again, see the datasheet for more info
        thermo_temperature = self.__getSensorTableValue(voltage) + room_temperature

        # if it's not in the range
        # then throw a ValueError exception - that simple!
        if not (thermo_temperature >= -70.0 and thermo_temperature <= 650.0):
            raise ValueError('temperature out of range')

        # and return the temperature value
        return thermo_temperature

    # private function which can't be accessed from the outside
    # can't get into details - the datasheet is your salvation
    # basically it calculates the voltage of the K-type sensor
    # before it gets into the amplifier - so the voltage is between -6.48 mV to 54.9 mV
    def __getThermocoupleVoltage(self):
        analog_value = grovepi.analogRead(self.thermocouple_pin);
        vout = analog_value / 1023.0 * 5 * 1000
        vin = (vout - self.__vol_offset) / self.__amp_av

        return vin

    # see the datasheet
    # the argument is the voltage of the K-Type sensor
    # before it enters the amplifier -> between -6.48 mV to 54.9 mV
    def __getSensorTableValue(self, mV):
        value = 0

        if mV > -6.478 and mV < 0:
            value = self.__sensor_table[0][8]

            for step in range(9, 0, -1):
                value = value * mV + self.__sensor_table[0][step - 1]

        elif mV >= 0 and mV < 20.644:
            value = self.__sensor_table[1][9]

            for step in range(10, 0, -1):
                value = value * mV + self.__sensor_table[1][step - 1]

        elif mV >= 20.644 and mV < 54.900:
            value = self.__sensor_table[2][6]

            for step in range(7, 0, -1):
                value = value * mV + self.__sensor_table[2][step - 2]

        return value

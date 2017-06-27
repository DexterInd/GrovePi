import grovepi
import math
import json
import numpy as np
from scipy.interpolate import interp1d

# Library written for Python 3!

# take a look in the datasheet
# http://www.mouser.com/catalog/specsheets/Seeed_111020002.pdf

# class for the K-Type temperature sensor (w/ long probe/sonde)
class HighTemperatureSensor:

    # initialize the object with the appropriate sensor pins on the GrovePi and configuration JSON
    def __init__(self, _temperature_pin, _thermocouple_pin, _json_path = None):
        
        if(_json_path is None):
            _json_path = 'thermocouple_table.json'

        try:
            with open(_json_path) as table_file:
                table = json.load(table_file)

            self.__interpolateTable(table)
            self.__amp_av = table["amp_factor"]
            self.__vol_offset = table["amp_offset"]

        except:
            self.sensor_table = None
            self.__amp_av = 1
            self.__vol_offset = 1
            self.voltage_to_degrees_table = None

        # save the variables inside the object
        self.temperature_pin = _temperature_pin
        self.thermocouple_pin = _thermocouple_pin

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
            pass
        analog_value = (analog_sum / 12) * voltage_ratio
        # see the datasheet for more information

        try:
            calculated_resistance = (1023 - analog_value) * 10000 / analog_value
            calculated_temperature = 1 / (math.log(calculated_resistance / 10000) / 3975 + 1 / 298.15) - 273.15

            # if the values exceed a certain threshold
            # then raise a ValueError exception
            if not (calculated_temperature >= -50.0 and calculated_temperature <= 145.0):
                raise ValueError('temperature out of range')

            # and return what we got calculated
            return calculated_temperature

        except ZeroDivisionError:

            return 0

    # function for retrieving the temperature at the tip of the probe / sonde
    # only the temperature of the tip of the probe is measured
    # the rest of the K-Type sensor is for reaching the hot environment you want to measure
    # so you don't get burned
    def getProbeTemperature(self):

        if not self.voltage_to_degrees_table is None:
            probe_tip_voltage = self.__getThermocoupleVoltage()
            degrees_from_table = self.voltage_to_degrees_table(probe_tip_voltage)

            return float(degrees_from_table)

        else:

            return None

    # private function which can't be accessed from the outside
    # this is an imperitave solution - it was found through experiments
    # basically it calculates the voltage of the K-type sensor
    # before it gets into the amplifier - so the voltage is between -6.48 mV to 54.9 mV
    def __getThermocoupleVoltage(self):
        analog_value = grovepi.analogRead(self.thermocouple_pin);
        probe_tip_voltage = (analog_value - self.__vol_offset) / self.__amp_av

        return probe_tip_voltage


    # function for interpolating values from [table] array
    def __interpolateTable(self, table):

        degrees_keys_list = list(table["degrees_table"].keys())
        degrees_list = [int(x) for x in degrees_keys_list]
        voltages_list = []

        for degrees in degrees_keys_list:
            voltage_corespondent = table["degrees_table"][degrees]
            voltages_list.append(voltage_corespondent)

        self.voltage_to_degrees_table = interp1d(voltages_list, degrees_list)

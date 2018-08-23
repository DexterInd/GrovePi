import smbus
import time
import math
import RPi.GPIO

"""
## License

The MIT License (MIT)
Copyright (c) 2016 Frederic Aguiard

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


class GroveI2CColorSensor:
    """ Provides access to the Grove I2C color sensor from Seeedstudio.

    This library supports 2 of the operating modes of the sensor:
    - Continuous, back-to-back color measures ('integrations') of pre-defined durations
    - Single measure of arbitrary duration
    The other sensor operating modes (using an external SYNC pin, interrupts...) which are not supported by this
    library.

    Usage:
    1. Use either use_continuous_integration() or use_manual_integration() to select operating mode
    2. If necessary, adjust gain and prescaler to obtain a color measure of sufficient precision without saturating the
       sensor.
    3. Start integration using start_integration()
    4. In manual integration mode: use stop_integration() after the desired duration
    5. Use one of the read functions to get the measured color value

    Reference documentation:
    - Seeedstudio wiki: http://www.seeedstudio.com/wiki/index.php?title=Twig_-_I2C_Color_Sensor_v0.9b
    - TCS3414-A Datasheet: http://www.seeedstudio.com/wiki/File:TCS3404_TCS3414-A.pdf
    """
    # Common colors coordinates (CIE xy and RGB)
    COLOR_TABLE = {"Red":           {"x": 0.64,  "y": 0.33,  "r": 255, "g": 0,   "b": 0},
                   "Green":         {"x": 0.3,   "y": 0.6,   "r": 0,   "g": 255, "b": 0},
                   "Blue":          {"x": 0.15,  "y": 0.06,  "r": 0,   "g": 0,   "b": 255},
                   "Yellow":        {"x": 0.419, "y": 0.505, "r": 255, "g": 255, "b": 0},
                   "Magenta":       {"x": 0.321, "y": 0.154, "r": 255, "g": 0,   "b": 255},
                   "Cyan":          {"x": 0.225, "y": 0.329, "r": 0,   "g": 255, "b": 255},
                   "Deep pink":     {"x": 0.466, "y": 0.238, "r": 255, "g": 20,  "b": 147},
                   "Orange":        {"x": 0.5,   "y": 0.441, "r": 255, "g": 165, "b": 0},
                   "Saddle brown":  {"x": 0.526, "y": 0.399, "r": 139, "g": 69,  "b": 19},
                   "Grey / White":  {"x": 0.313, "y": 0.329, "r": 255, "g": 255, "b": 255},
                   "Black":         {"x": 0,     "y": 0,     "r": 0,   "g": 0,   "b": 0}}

    # Sensor address on SMBus / I2C bus
    _I2C_SENSOR_ADDRESS = 0X39

    # Sensor registers addresses
    _REGISTER_COMMAND = 0X80
    _REGISTER_CONTROL = _REGISTER_COMMAND | 0X00
    _REGISTER_TIMING = _REGISTER_COMMAND | 0X01
    _REGISTER_INTERRUPT_CONTROL = _REGISTER_COMMAND | 0X02
    _REGISTER_INT_SOURCE = _REGISTER_COMMAND | 0X03
    _REGISTER_ID = _REGISTER_COMMAND | 0X04
    _REGISTER_GAIN = _REGISTER_COMMAND | 0X07
    _REGISTER_INTERRUPT_LOW_THRESH_LOW_BYTE = _REGISTER_COMMAND | 0X08
    _REGISTER_INTERRUPT_LOW_THRESH_HIGH_BYTE = _REGISTER_COMMAND | 0X09
    _REGISTER_INTERRUPT_HIGH_THRESH_LOW_BYTE = _REGISTER_COMMAND | 0X0A
    _REGISTER_INTERRUPT_HIGH_THRESH_HIGH_BYTE = _REGISTER_COMMAND | 0X0B
    _REGISTER_DATA_GREEN_LOW = _REGISTER_COMMAND | 0X10
    _REGISTER_DATA_GREEN_HIGH = _REGISTER_COMMAND | 0X11
    _REGISTER_DATA_RED_LOW = _REGISTER_COMMAND | 0X012
    _REGISTER_DATA_RED_HIGH = _REGISTER_COMMAND | 0X13
    _REGISTER_DATA_BLUE_LOW = _REGISTER_COMMAND | 0X14
    _REGISTER_DATA_BLUE_HIGH = _REGISTER_COMMAND | 0X15
    _REGISTER_DATA_CLEAR_LOW = _REGISTER_COMMAND | 0X16
    _REGISTER_DATA_CLEAR_HIGH = _REGISTER_COMMAND | 0X17
    _REGISTER_INTERRUPT_CLEAR = _REGISTER_COMMAND | 0X60

    # Values for control register
    _CONTROL_ADC_IS_VALID = 0X10
    _CONTROL_ADC_ENABLE = 0X02
    _CONTROL_ADC_DISABLE = 0X00
    _CONTROL_ADC_POWER_ON = 0X01
    _CONTROL_ADC_POWER_OFF = 0X00

    # Values for timing register
    _TIMING_SYNC_EDGE = 0X40
    _TIMING_INTEGRATION_MODE_CONTINUOUS = 0X00
    _TIMING_INTEGRATION_MODE_MANUAL = 0X10
    _TIMING_INTEGRATION_MODE_SYNC_SINGLE_PULSE = 0X20
    _TIMING_INTEGRATION_MODE_SYNC_MULTIPLE_PULSE = 0X30
    _TIMING_PARAM_INTEGRATION_TIME_12MS = 0X00
    _TIMING_PARAM_INTEGRATION_TIME_100MS = 0X01
    _TIMING_PARAM_INTEGRATION_TIME_400MS = 0X02
    _TIMING_PARAM_SYNC_PULSE_COUNT_1 = 0X00
    _TIMING_PARAM_SYNC_PULSE_COUNT_2 = 0X01
    _TIMING_PARAM_SYNC_PULSE_COUNT_4 = 0X02
    _TIMING_PARAM_SYNC_PULSE_COUNT_8 = 0X03
    _TIMING_PARAM_SYNC_PULSE_COUNT_16 = 0X04
    _TIMING_PARAM_SYNC_PULSE_COUNT_32 = 0X05
    _TIMING_PARAM_SYNC_PULSE_COUNT_64 = 0X06
    _TIMING_PARAM_SYNC_PULSE_COUNT_128 = 0X07
    _TIMING_PARAM_SYNC_PULSE_COUNT_256 = 0X08

    # Values for interrupt control register
    _INTERRUPT_CONTROL_MODE_DISABLE = 0X00
    _INTERRUPT_CONTROL_MODE_LEVEL = 0X10
    _INTERRUPT_CONTROL_MODE_SMB_ALERT = 0x20
    _INTERRUPT_CONTROL_PERSIST_EVERY_CYCLE = 0X00
    _INTERRUPT_CONTROL_PERSIST_OUTSIDE_RANGE_ONCE = 0X01
    _INTERRUPT_CONTROL_PERSIST_OUTSIDE_RANGE_100MS = 0X02
    _INTERRUPT_CONTROL_PERSIST_OUTSIDE_RANGE_1000MS = 0X03

    # Values for interrupt source register
    _INTERRUPT_SOURCE_GREEN = 0X00
    _INTERRUPT_SOURCE_RED = 0X01
    _INTERRUPT_SOURCE_BLUE = 0X10
    _INTERRUPT_SOURCE_CLEAR = 0X03

    # Values for gain register
    _GAIN_1X = 0X00
    _GAIN_4X = 0X10
    _GAIN_16X = 0X20
    _GAIN_64X = 0X30
    _PRESCALER_1 = 0X00
    _PRESCALER_2 = 0X01
    _PRESCALER_4 = 0X02
    _PRESCALER_8 = 0X03
    _PRESCALER_16 = 0X04
    _PRESCALER_32 = 0X05
    _PRESCALER_64 = 0X06

    # Wait time introduced after each register write (except integration start)
    _SLEEP_VALUE = 0.05

    def __init__(self, bus_number=None):
        """Initialize i2c communication with the sensor and sets default parameters.

        Default parameters: continuous integration (not started) with 12ms cycles, gain 1x, pre-scale 1.

        :param bus_number: the i2c bus number (usually 0 or 1, depending on the hardware). Use the i2cdetect command
        line tool to identify the right bus. If set to None, will use the Raspberry Pi revision number to guess which
        bus to use.
        """
        if bus_number is None:
            # Use Rasbperry Pi revision to choose bus number
            board_revision = RPi.GPIO.RPI_REVISION
            if board_revision == 2 or board_revision == 3:
                bus_number = 1
            else:
                bus_number = 0
        self.bus = smbus.SMBus(bus_number)
        self.use_continuous_integration()
        self.set_gain_and_prescaler(1, 1)

    def use_continuous_integration(self, integration_time_in_ms=12):
        """Configure the sensor to perform continuous, back-to-back integrations of pre-defined duration.
        Continuous integration will begin after calling start_integration() and will stop after calling
        stop_integration().

        :param integration_time_in_ms: supported values in ms are 12, 100 and 400.
        """
        assert integration_time_in_ms == 12 \
            or integration_time_in_ms == 100 \
            or integration_time_in_ms == 400, \
            "Continuous integration supports only 12ms, 100ms or 400ms integration durations"

        # Convert integration time value into the corresponding byte values expected by the sensor.
        if integration_time_in_ms == 12:
            integration_time_reg = self._TIMING_PARAM_INTEGRATION_TIME_12MS
        elif integration_time_in_ms == 100:
            integration_time_reg = self._TIMING_PARAM_INTEGRATION_TIME_100MS
        elif integration_time_in_ms == 400:
            integration_time_reg = self._TIMING_PARAM_INTEGRATION_TIME_400MS
        else:
            integration_time_reg = self._TIMING_PARAM_INTEGRATION_TIME_12MS

        self.bus.write_i2c_block_data(self._I2C_SENSOR_ADDRESS,
                                      self._REGISTER_TIMING,
                                      [self._TIMING_INTEGRATION_MODE_CONTINUOUS | integration_time_reg])
        time.sleep(self._SLEEP_VALUE)

    def use_manual_integration(self):
        """Configure the sensor to perform a single integration manually started and stopped.

        Manual integration will begin after calling start_integration(), and will stop after calling stop_integration().
        """
        self.bus.write_i2c_block_data(self._I2C_SENSOR_ADDRESS,
                                      self._REGISTER_TIMING,
                                      [self._TIMING_INTEGRATION_MODE_MANUAL])
        time.sleep(self._SLEEP_VALUE)

    def set_gain_and_prescaler(self, gain_multiplier=1, prescaler_divider=1):
        """Configure the sensor gain and prescaler.

        :param gain_multiplier: Gain sets the sensibility of the sensor, effectively extending the dynamic range of the
        sensor but eventually inducing saturation. Supported values are 1, 4, 16 and 64.

        :param prescaler_divider: Prescaler scales the values by dividing them before storage in the output registers,
        hence reducing saturation at the cost of reducing measurement precision. Supported prescaler dividers are 1, 2,
        4, 8, 16, 32 and 64.
        """
        assert gain_multiplier == 1 or gain_multiplier == 4 or gain_multiplier == 16 or gain_multiplier == 64, \
            "Supported gain multipliers: 1, 4, 16 and 64"
        assert prescaler_divider == 1 \
            or prescaler_divider == 2 \
            or prescaler_divider == 4 \
            or prescaler_divider == 8 \
            or prescaler_divider == 16 \
            or prescaler_divider == 32 \
            or prescaler_divider == 64, \
            "Supported prescaler dividers: 1, 2, 4, 8, 16, 32 and 64"

        # Convert gain multiplier into the corresponding byte values expected by the sensor.
        if gain_multiplier == 1:
            gain_reg = self._GAIN_1X
        elif gain_multiplier == 4:
            gain_reg = self._GAIN_4X
        elif gain_multiplier == 16:
            gain_reg = self._GAIN_16X
        elif gain_multiplier == 64:
            gain_reg = self._GAIN_64X
        else:
            gain_reg = self._GAIN_1X

        # Convert prescaler divider into the corresponding byte values expected by the sensor.
        if prescaler_divider == 1:
            prescaler_reg = self._PRESCALER_1
        elif prescaler_divider == 2:
            prescaler_reg = self._PRESCALER_2
        elif prescaler_divider == 4:
            prescaler_reg = self._PRESCALER_4
        elif prescaler_divider == 8:
            prescaler_reg = self._PRESCALER_8
        elif prescaler_divider == 16:
            prescaler_reg = self._PRESCALER_16
        elif prescaler_divider == 32:
            prescaler_reg = self._PRESCALER_32
        elif prescaler_divider == 64:
            prescaler_reg = self._PRESCALER_64
        else:
            prescaler_reg = self._PRESCALER_1

        self.bus.write_i2c_block_data(self._I2C_SENSOR_ADDRESS, self._REGISTER_GAIN, [gain_reg | prescaler_reg])
        time.sleep(self._SLEEP_VALUE)

    def start_integration(self):
        """Start the integration.
        """
        self.bus.write_i2c_block_data(
            self._I2C_SENSOR_ADDRESS,
            self._REGISTER_CONTROL,
            [self._CONTROL_ADC_ENABLE | self._CONTROL_ADC_POWER_ON])

    def stop_integration(self):
        """Stop the integration.
        """
        self.bus.write_i2c_block_data(
            self._I2C_SENSOR_ADDRESS,
            self._REGISTER_CONTROL,
            [self._CONTROL_ADC_DISABLE | self._CONTROL_ADC_POWER_ON])

    def is_integration_complete(self):
        """ Checks if an integration has been successfully completed and color data is ready to be read.

        :return: True if integration is completed.
        """
        integration_status = self.bus.read_i2c_block_data(self._I2C_SENSOR_ADDRESS, self._REGISTER_CONTROL, 1)
        return integration_status[0] & self._CONTROL_ADC_IS_VALID == self._CONTROL_ADC_IS_VALID

    def read_rgbc_word(self):
        """ Reads the measured color, split over 4 channels: red, green, blue, clear.
        Each value is provided as a word.

        :return: a (r,g,b,c) tuple of the 4 word values measured by the red/green/blue/clear channels
        """
        # Integration result registers are 8 consecutive bytes starting by lower value of green channel.
        # Reading them in a single pass.
        raw_color = self.bus.read_i2c_block_data(self._I2C_SENSOR_ADDRESS, self._REGISTER_DATA_GREEN_LOW, 8)

        return (raw_color[2] + raw_color[3] * 256,
                raw_color[0] + raw_color[1] * 256,
                raw_color[4] + raw_color[5] * 256,
                raw_color[6] + raw_color[7] * 256)

    def read_rgbc(self):
        """ Reads the measured color, split over 4 channels: red, green, blue, clear (unfiltered).
        Each value is provided as a byte.

        :return: a (r,g,b,c) tuple of the 4 byte values measured by the red/green/blue/clear channels
        """
        # Integration result registers are 8 consecutive bytes starting by lower value of green channel.
        # Reading them in a single pass.
        raw_color = self.bus.read_i2c_block_data(self._I2C_SENSOR_ADDRESS, self._REGISTER_DATA_GREEN_LOW, 8)

        # Discard lower byte of each channel
        return (raw_color[3],
                raw_color[1],
                raw_color[5],
                raw_color[7])

    def read_xy(self):
        """ Reads the measured color and converts it as CIE x,y coordinates.

        See http://www.techmind.org/colour/ and https://en.wikipedia.org/wiki/CIE_1931_color_space for more information.

        :return: a (x, y) tuple
        """
        rgbc = self.read_rgbc_word()
        x_bar = -0.14282 * rgbc[0] + 1.54924 * rgbc[1] + -0.95641 * rgbc[2]
        y_bar = -0.32466 * rgbc[0] + 1.57837 * rgbc[1] + -0.73191 * rgbc[2]
        z_bar = -0.68202 * rgbc[0] + 0.77073 * rgbc[1] + 0.563320 * rgbc[2]

        x = x_bar / (x_bar + y_bar + z_bar)
        y = y_bar / (x_bar + y_bar + z_bar)

        return [x, y]

    def read_color_name(self):
        """ Reads the measured color and maps it to the nearest color present in COLOR_TABLE.

        Warning: current implementation does not work well with white / grey / black or dark colors.

        :return: The color name used as a key in COLOR_TABLE.
        """
        xy = self.read_xy()
        closest_color = None
        closest_distance = 1
        for current_color in self.COLOR_TABLE:
            current_coordinates = self.COLOR_TABLE[current_color]
            current_dist = math.sqrt(
                    (current_coordinates["y"] - xy[1])**2 + (current_coordinates["x"] - xy[0])**2)
            if current_dist < closest_distance:
                closest_color = current_color
                closest_distance = current_dist

        return closest_color

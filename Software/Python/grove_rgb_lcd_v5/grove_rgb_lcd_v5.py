from time import sleep
from i2cdevice import Device, Register, BitField
from i2cdevice.adapter import Adapter

class PercentAdapter(Adapter):
    def _decode(self, value):
        return value/2.56

    def _encode(self, value):
        if value <= 0:
            return 0
        elif value >= 99.609375:
            return 0xff
        else:
            return round(value*2.56)
             

class TimeAdapter(Adapter):
    def _decode(self, value):
        if value == 0:
            return 0.128
        else:
            return 0.384 + 0.128*(value-1)

    def _encode(self, value):
        if value <= 0.256:
            return 0
        elif value <= 0.384:
            return 1
        elif value >= 16.512:
            return 127
        else:
            return int(round(value/0.128) - 2)

class ShortTimeAdapter(Adapter):
    def _decode(self, value):
        if value == 0:
            return 1.5
        else:
            return 96*value

    def _encode(self, value):
        value = 0.128*round(value/0.128)
        if value <= 47.25:
            return 0
        elif value >= 1440:
            return 0xf
        else:
            return round(value/96)

class RgbLcd:
    def __init__(self, i2c_dev=None, i2c_rgb_addr=(0x30), i2c_lcd_addr=(0x7c>>1)):
        self._is_setup = False
        self._i2c_rgb_addr = i2c_rgb_addr
        self._i2c_lcd_addr = i2c_lcd_addr

        if i2c_dev is None:
            import smbus2
            self._i2c_dev = smbus2.SMBus(1)
        else:
            self._i2c_dev = i2c_dev
            
        self._i2c_lcd = self._i2c_dev
            
        self._displayfunction = 0x08
        self._displaycontrol = 0x04
        self._displaymode = 0x02
        self._cursorshift = 0x04
        self._cursorpos = 0x00

        self._channel_led1 = None
        self._channel_led2 = None
        self._channel_led3 = None

        self._i2c_rgb = Device(self._i2c_rgb_addr, i2c_dev=self._i2c_dev, bit_width=8, registers=(
            Register("EN_RST", 0x00, volatile=False, fields=(
                BitField("tctrl_rst", 0b00000111), # 0-3, Time Slot Control; 4, Nothing; 5, Reset registers; 6, Main Digital; 7, Reset All;
                BitField("enable_ctrl", 0b00011000), # Shutdow control
                BitField("rise_fall", 0b01100000), # These two bits allow to scale the rise and fall time defined in Reg5 ramp rate register: 0, Normal; 1, 2x Slower; 2, 4x Slower; 3, 8x Faster;
            )),
            Register("FLASH_PERIOD", 0x01, volatile=False, fields=(
                BitField("period", 0b01111111, adapter=TimeAdapter()),
                BitField("ramp_linear", 0b10000000), # 0, logarithmic-like S ramp up and down curve; 1, linear up and down waveform;
            )),
            Register("PWM1_TIMER", 0x02, volatile=False, fields=(
                BitField("period", 0b11111111, adapter=PercentAdapter()), # int(period\256*100%)
            )),
            Register("PWM2_TIMER", 0x03, volatile=False, fields=(
                BitField("period", 0b11111111, adapter=PercentAdapter()), # int(period\256*100%)
            )),
            Register("CHANNEL_CTRL", 0x04, volatile=False, fields=(
                BitField("led1", 0b00000011), # 00, off; 01, on; 10, pmw1; 11, pmw2;
                BitField("led2", 0b00001100), # 00, off; 01, on; 10, pmw1; 11, pmw2;
                BitField("led3", 0b00110000), # 00, off; 01, on; 10, pmw1; 11, pmw2;
            )),
            Register("RAMP_RATE", 0x05, volatile=False, fields=(
                BitField("l_rise", 0b00001111, adapter=ShortTimeAdapter()), # ms
                BitField("l_fall", 0b11110000, adapter=ShortTimeAdapter()), # ms
            )),
            Register("LED1_IOUT", 0x06, volatile=False, fields=(
                BitField("iout", 0b11111111), # 0-191, 0.25-24mA;
            )),
            Register("LED2_IOUT", 0x07, volatile=False, fields=(
                BitField("iout", 0b11111111), # 0-191, 0.25-24mA;
            )),
            Register("LED3_IOUT", 0x08, volatile=False, fields=(
                BitField("iout", 0b11111111), # 0-191, 0.25-24mA;
            ))

        ))

    def setup(self):
        if self._is_setup:
            return

        self._is_setup = True

        self._i2c_rgb.select_address(self._i2c_rgb_addr)

        try:
            self._i2c_rgb.set("EN_RST", tctrl_rst=0b111)
            sleep(0.01)
            self.pwmmode(0)
            self.setchannel(0, 0, 0)
            self.setrgb(0,0,0)
            self.pwmtime(1)
            self.pwmpercent(50, 50)
            self.risefall(0,0,0,0)
            
            sleep(0.1)
            self._command(0x20 | self._displayfunction)
            sleep(0.1)
            self._command(0x20 | self._displayfunction)
            sleep(0.1)
            self._command(0x20 | self._displayfunction)
            sleep(0.1)
            self._command(0x08 | self._displaycontrol)
            sleep(0.2)
            self._command(0x01)
            sleep(0.2)
            self._command(0x04 | self._displaymode);
            sleep(0.1)
        except IOError as e:
            raise RuntimeError(f"Error inizializing Grove-LCD RGB Backligh' on 0x{self._i2c_lcd_addr:02x} and 0x{self._i2c_rgb_addr:02x}, {e}")
        except Exception as e:
            raise e

    def setrgb(self, r, g, b):
        self.setup()

        r &= 0xff
        g &= 0xff
        b &= 0xff

        r_map = int((r-1)/254*191)
        g_map = int((g-1)/254*191)
        b_map = int((b-1)/254*191) 

        if r != 0 and self._i2c_rgb.get("LED1_IOUT").iout != r_map:
            self._i2c_rgb.set("LED1_IOUT", iout=r_map)
        if g != 0 and self._i2c_rgb.get("LED2_IOUT").iout != g_map:
            self._i2c_rgb.set("LED2_IOUT", iout=g_map)
        if b != 0 and self._i2c_rgb.get("LED3_IOUT").iout != b_map:
            self._i2c_rgb.set("LED3_IOUT", iout=b_map)

        led1 = self._channel_led1 if r != 0 else 0
        led2 = self._channel_led2 if g != 0 else 0
        led3 = self._channel_led3 if b != 0 else 0

        if {"led1":led1, "led2":led2, "led3":led2} != self._i2c_rgb.get("CHANNEL_CTRL"):
            self._i2c_rgb.set("CHANNEL_CTRL", led1=led1, led2=led2, led3=led3)

    def setchannel(self, r=None,g=None,b=None):
        self.setup()

        if r is g is b is None:
            return
        
        options = {
            "default":	1,
            "pmw1":		2,
            "pmw2":		3
        }
        
        kwargs = {}
        
        for key, value in [('led1', r), ('led2', g), ('led3', b)]:
            if value is not None:
                if value in options:
                    kwargs[key] = options.get(value)
                elif isinstance(value, int):
                    kwargs[key] = value%4 +1

                setattr(self, f"_channel_{key}", kwargs.get(key))
                if getattr(self._i2c_rgb.get("CHANNEL_CTRL"), key) == 0:
                    kwargs[key] = 0
        
        diff = False
        for key,value in kwargs.items():
            if value != getattr(self._i2c_rgb.get("CHANNEL_CTRL"), key):
                diff = True
                break

        if diff:
            self._i2c_rgb.set("CHANNEL_CTRL", **kwargs)

    def pwmmode(self, mode=None):
        """
        Controls the pwm mode.
        
        Cx is the pwm channel
        PWMx is the pwm option reg
        
        If any off the options generate a sequence that exceeds 100% of the period, it will be cut off at 100%

        param mode:
            -0 C1 and C2 blink for PWM1% of the period time. PWM2 is disabled
            -1 C1 blinks for PWM1% of the period time, then C2 blinks for PWM2% of the period time.
            -2 C1 blinks for PWM1% of the period time, then nothing blinks for PWM2% of the period time, then C2 blinks for PWM1% of the period time.
            -3 C1 blinks for PWM1% of the period time, then nothing blinks for PWM1% of the period, then C2 blinks for PWM2% of the period time, then nothing blinks for PMW2% of the period time
        """
        self.setup()
        
        if mode is None:
            mode = (self._i2c_rgb.get("EN_RST").tctrl_rst + 1) % 4
        else:
            mode &= 0b11
        
        if mode != self._i2c_rgb.get("EN_RST").tctrl_rst:
            self._i2c_rgb.set("EN_RST", tctrl_rst=mode)
            
    
    def pwmtime(self, time):
        self.setup()
        self._i2c_rgb.set("FLASH_PERIOD", period=time)
    
    def risefall(self, rise=None, fall=None, mult=None, lin=None):
        self.setup()
        if not rise is fall is None:
            kwargs = {k: v for k,v in [[('l_rise'), rise],[('l_fall'), fall]] if v is not None}
            if kwargs:
                self._i2c_rgb.set("RAMP_RATE", **kwargs)
                
        if mult is not None:
            mult %=4
            if self._i2c_rgb.get("EN_RST").rise_fall != mult:
                self._i2c_rgb.set("EN_RST", rise_fall=mult)
        
        if lin is not None:
            if lin:
                lin = 1
            if self._i2c_rgb.get("FLASH_PERIOD").ramp_linear != lin:
                self._i2c_rgb.set("FLASH_PERIOD", ramp_linear=lin)
    
    def pwmpercent(self, pwm1=None, pwm2=None):
        self.setup()
        if pwm1 is not None:
            self._i2c_rgb.set("PWM1_TIMER", period=pwm1)
        if pwm2 is not None:
            self._i2c_rgb.set("PWM2_TIMER", period=pwm2)


    def _command(self, value):
        self.setup()
        self._i2c_lcd.write_byte_data(self._i2c_lcd_addr, 0x80, value)
    
    def clear(self):
        """
        Clear the display and reset the displayshift and cursorposition.
        """
        self._cursorpos = 0x00
        self._command(0x01)
        sleep(0.01)
        
    def home(self):
        """
        Reset the displayshift and cursorposition.
        """
        self._cursorpos = 0x00
        self._command(0x02)
        sleep(0.01)
    
    def setcursor(self, col, row):
        """
        Set the cursorposition.
        
        param col:
            -set to the preffered collumn number
        param row:
            -set to teh preffered row
        """
        col = col % 0x180 if row == 0 else (col | 0xc0) %0x180
        self._cursorpos = col
        self._command(0x80 | col)
    
    def display(self, value=None):
        """
        Control display state.
        
        param value:
            -set to False, 0 or "off" to disable display.
            -set to True, 1 or "on" to enable display.
            -set to None to toggle.
        """
        if value is None:
            value = not self._displaycontrol&0x04 == 0x04
        elif isinstance(value, str):
            if value == "on":
                value = True
            elif value == "off":
                value = False
            else:
                raise ValueError("Invalid option. For more information use help()")

        if value:
            self._displaycontrol |= 0x04
        else:
            self._displaycontrol &= ~0x04

        self._command(0x08 | self._displaycontrol)
    
    def cursor(self, value=None):
        """
        Control the cursor state.
        
        param value:
            -set to False, 0 or "off" to disable the cursor.
            -set to True, 1 or "on" to enable the cursor.
            -set to None to toggle.
        """
        if value is None:
            value = not self._displaycontrol&0x02 == 0x02
        elif isinstance(value, str):
            if value == "on":
                value = True
            elif value == "off":
                value = False
            
        if value:
            self._displaycontrol |= 0x02
        else:
            self._displaycontrol &= ~0x02
            
        self._command(0x08 | self._displaycontrol)
    
    def blink(self, value=None):
        """
        Control the cursorblink functionallity.
        
        param value:
            -set to False, 0 or "off" to disable cursorblinking.
            -set to True, 1 or "on" to enable cursorblinking.
            -set to None to toggle.
        """
        if value is None:
            value = not self._displaycontrol&0x01 == 0x01
        elif isinstance(value, str):
            if value == "on":
                value = True
            elif value == "off":
                value = False
            
        if value:
            self._displaycontrol |= 0x01
        else:
            self._displaycontrol &= ~0x01
            
        self._command(0x08 | self._displaycontrol)
        
    def displayshift(self, value=None):
        """
        Shift the display one step in a direcion.
        
        param value:
            -set to False, 0, or "left" to shift the display one step left.
            -set to True, 1, or "right" to shift the display one step right.
            -set to None to shift one step in the previous direction.
        """
        if value is None:
            value = self._cursorshift&0x04
        elif isinstance(value, str):
            if value == "right":
                value = True
            elif value == "left":
                value = False
            
        if value:
            self._cursorshift |= 0x04
        else:
            self._cursorshift &= ~0x04
            
        self._cursorshift |= 0x08
        self._command(0x10 | self._cursorshift)
        
    def cursorshift(self, value=None):
        """
        Shift the cursor one step in a direcion.
        
        param value:
            -set to False, 0, or "left" to shift the cursor one step left.
            -set to True, 1, or "right" to shift the cursor one step right.
            -set to None to shift one step in the previous direction.
        """
        if value is None:
            value = self._cursorshift&0x04
        elif isinstance(value, str):
            if value == "right":
                value = True
            elif value == "left":
                value = False
            
        if value:
            self._cursorshift |= 0x04
            self._cursorpos = (self._cursorpos + 1) % 0x180
        else:
            self._cursorshift &= ~0x04
            self._cursorpos = (self._cursorpos - 1) % 0x180
        
        self._cursorshift &= ~0x08
        self._command(0x10 | self._cursorshift)
        
    
    def texthead(self, value=None):
        """
        Control the direction (heading) text is typed.
        
        param value:
            -set to False, 0, or "left" make new chacacters appear left from the previous.
            -set to True, 1, or "right" make new chacacters appear right from the previous.
            -set to None to toggle.
        """
        if value is None:
            value = not self._displaymode&0x02 == 0x02
        elif isinstance(value, str):
            if value == "right":
                value = True
            elif value == "left":
                value = False
            
        if value:
            self._displaymode |= 0x02
        else:
            self._displaymode &= ~0x02
            
        self._command(0x04 | self._displaymode)
    
    def autoscroll(self, value=None):
        """
        Control the autosroll functionallity.
        
        param value:
            -set to False, 0 or "off" to disable autoscroll functionallity.
            -set to True, 1 or "on" to enable autoscroll functionality.
            -set to None to toggle.
        """
        if value is None:
            value = not self._displaymode&0x01 == 0x01
        elif isinstance(value, str):
            if value == "on":
                value = True
            elif value == "off":
                value = False
            
        if value:
            self._displaymode |= 0x01
        else:
            self._displaymode &= ~0x01
            
        self._command(0x04 | self._displaymode)
    
    def createchar(self, location, charmap):
        """
        Create a custom character at a chosen location
        
        param location:
            -set to the location at witch you want the custom character stored. Value can range from 0-7
        param charmap:
            -set to the charmap of your custom character. Format must be a 5x8 list, bitlist or number.
        """
        self.setup()

        if isinstance(charmap, int):
            if charmap == 0:
                charmap = [0]
            else:
                charmap = list(charmap.to_bytes((charmap.bit_length()+7) // 8, "big"))
        elif isinstance(charmap, list):
            for item in range(len(charmap)):
                if isinstance(charmap[item], list):
                    tmp = 0
                    for num in range(len(charmap[item])):
                        tmp += charmap[item][num] << num
                    charmap[item] = tmp
                charmap[item] = charmap[item] & 0xff
        
        location &= 0x7
        self._command(0x40 | (location << 3))
        self._i2c_lcd.write_i2c_block_data(self._i2c_lcd_addr, 0x40, charmap[:8])
        self.setcursor(self._cursorpos, 0)
        
    def write(self, value):
        """
        Write to the lcd.
        
        param value:
            -Input an int, str or list an it will be converted as good as possible to a bytelist, whitch will be written to the lcd"
        """
        self.setup()
        
        if isinstance(value, str):
            value = list(value)
            for letter in range(len(value)):
                value[letter] = ord(value[letter])  
        elif isinstance(value, int):
            if value == 0:
                value = [0]
            else:
                value = list(value.to_bytes((value.bit_length()+7) // 8, "big"))
        elif isinstance(value, list):
            for item in range(len(value)):
                if isinstance(value[item], str):
                    value[item] = ord(value[item][0])
                elif isinstance(value[item], int):
                    value[item] = value[item] & 0xff
                elif isinstance(value, list):
                    raise ValueError("You cannot write lists.")
        
        if len(value) > 32:
            raise ValueError("The maximum data that can be written is 32 bytes!")
        
        if self._displaymode&0x02 == 0x02:
            self._cursorpos = (self._cursorpos + len(value)) % 0x180
        else:
            self._cursorpos = (self._cursorpos - len(value)) % 0x180
        self._i2c_lcd.write_i2c_block_data(self._i2c_lcd_addr, 0x40, value)

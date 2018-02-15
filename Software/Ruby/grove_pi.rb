#!/usr/bin/env ruby

module GrovePi
  require 'i2c'
  require 'i2c/driver/i2c-dev'

  # Commands.
  CMD_READ_DIGITAL = 1
  CMD_WRITE_DIGITAL = 2
  CMD_READ_ANALOG = 3
  CMD_WRITE_ANALOG = 4
  CMD_PIN_MODE = 5
  CMD_READ_FIRMWARE_VERSION = 8

  # Arduino pin mappings.
  PIN_ANALOG_A0 = 14
  PIN_ANALOG_A1 = 15
  PIN_ANALOG_A2 = 16
  PIN_DIGITAL_D2 = 2
  PIN_DIGITAL_D3 = 3
  PIN_DIGITAL_D4 = 4
  PIN_DIGITAL_D5 = 5
  PIN_DIGITAL_D6 = 6
  PIN_DIGITAL_D7 = 7
  PIN_DIGITAL_D8 = 8

  # Pin modes.
  PIN_MODE_IN = 0
  PIN_MODE_OUT = 1

  # Configuration settings.
  CONFIG_RETRIES = 10
  GROVE_PI_I2C_SLAVE_ADDRESS = 4

  # The initialized I2C object.
  @_i2c_grove_pi = nil

  # Storage for I2C slave addresses present on ports I2C-1, I2C-2 or I2C-3.
  @_i2c_slave_addresses = Hash.new

  # Internal functions.
  #
  # These functions are not intended to be used directly by the user but by the
  # functions which are exposed to the user.
  def self._grove_pi_discover()
    begin
      i2c_device_files = Dir['/dev/i2c-*']

      if i2c_device_files.length < 1
        return false, nil
      end

      # Iterate over I2C device files.
      for f in i2c_device_files
        device_file = f
        f = f.strip
        f.slice! '/dev/i2c-'
        lines = %x(#{'i2cdetect -y ' + Integer(f).to_s}).split("\n")

        # Get rid of the first line.
        lines.shift

        if lines.length < 1
          next
        end

        # Process i2cdetect command output for the I2C device file.
        for i in 0..lines.length - 1
          line = lines[i].strip
          line = line.split ':'

          if line.length != 2
            next
          end

          for i2c_address in line[1].split(' ')
            begin
              if Integer(i2c_address) == GROVE_PI_I2C_SLAVE_ADDRESS
                return true, device_file.strip
              end
            rescue
              next
            end
          end
        end
      end
    rescue
      return false, nil
    end

    return false, nil
  end

  def self._grove_pi_init()
    status, i2c_device_file = self._grove_pi_discover

    if status && i2c_device_file != nil
      return I2CDevice.new address: GROVE_PI_I2C_SLAVE_ADDRESS,
                           driver: I2CDevice::Driver::I2CDev.new(i2c_device_file)
    else
      return nil
    end
  end

  def self._ensure_init()
    if @_i2c_grove_pi == nil
      @_i2c_grove_pi = self._grove_pi_init

      if @_i2c_grove_pi == nil
        raise 'No GrovePi found.'
      end
    end
  end

  def self._set_pin_mode(pin, mode)
    self._ensure_init
    @_i2c_grove_pi.i2cset @_i2c_grove_pi.address, CMD_PIN_MODE, pin, mode, 0
  end

  def self._read_analog(pin)
    self._ensure_init
    @_i2c_grove_pi.i2cset @_i2c_grove_pi.address, CMD_READ_ANALOG, pin, 0, 0
    bytes = @_i2c_grove_pi.i2cget(@_i2c_grove_pi.address, 3).chars
    return (bytes[1].ord * 256) + bytes[2].ord
  end

  def self._write_analog(pin, value)
    self._ensure_init
    @_i2c_grove_pi.i2cset @_i2c_grove_pi.address, CMD_WRITE_ANALOG, pin, value, 0
  end

  def self._read_digital(pin)
    self._ensure_init
    @_i2c_grove_pi.i2cset @_i2c_grove_pi.address, CMD_READ_DIGITAL, pin, 0, 0
    return @_i2c_grove_pi.i2cget(@_i2c_grove_pi.address, 2).chars[0].ord
  end

  def self._write_digital(pin, value)
    self._ensure_init
    @_i2c_grove_pi.i2cset @_i2c_grove_pi.address, CMD_WRITE_DIGITAL, pin, value, 0
  end

  # Functions exposed to the user.

  # Analog read functions.
  def self.read_analog_A0()
    for i in 0..CONFIG_RETRIES - 1
      begin
        self._set_pin_mode PIN_ANALOG_A0, PIN_MODE_IN
        return self._read_analog PIN_ANALOG_A0
      rescue Errno::EREMOTEIO
        next
      end
    end
  end

  def self.read_analog_A1()
    for i in 0..CONFIG_RETRIES - 1
      begin
        self._set_pin_mode PIN_ANALOG_A1, PIN_MODE_IN
        return self._read_analog PIN_ANALOG_A1
      rescue Errno::EREMOTEIO
        next
      end
    end
  end

  def self.read_analog_A2()
    for i in 0..CONFIG_RETRIES - 1
      begin
        self._set_pin_mode PIN_ANALOG_A2, PIN_MODE_IN
        return self._read_analog PIN_ANALOG_A2
      rescue Errno::EREMOTEIO
        next
      end
    end
  end

  # Analog write functions (PWM on digital pins D3, D5 and D6).
  def self.write_analog_D3(value)
    for i in 0..CONFIG_RETRIES - 1
      begin
        self._set_pin_mode PIN_DIGITAL_D3, PIN_MODE_OUT
        self._write_analog PIN_DIGITAL_D3, value
        return
      rescue Errno::EREMOTEIO
        next
      end
    end
  end

  def self.write_analog_D5(value)
    for i in 0..CONFIG_RETRIES - 1
      begin
        self._set_pin_mode PIN_DIGITAL_D5, PIN_MODE_OUT
        self._write_analog PIN_DIGITAL_D5, value
        return
      rescue Errno::EREMOTEIO
        next
      end
    end
  end

  def self.write_analog_D6(value)
    for i in 0..CONFIG_RETRIES - 1
      begin
        self._set_pin_mode PIN_DIGITAL_D6, PIN_MODE_OUT
        self._write_analog PIN_DIGITAL_D6, value
        return
      rescue Errno::EREMOTEIO
        next
      end
    end
  end

  # Digital read functions.
  def self.read_digital_D2()
    for i in 0..CONFIG_RETRIES - 1
      begin
        self._set_pin_mode PIN_DIGITAL_D2, PIN_MODE_IN
        return self._read_digital PIN_DIGITAL_D2
      rescue Errno::EREMOTEIO
        next
      end
    end
  end

  def self.read_digital_D3()
    for i in 0..CONFIG_RETRIES - 1
      begin
        self._set_pin_mode PIN_DIGITAL_D3, PIN_MODE_IN
        return self._read_digital PIN_DIGITAL_D3
      rescue Errno::EREMOTEIO
        next
      end
    end
  end

  def self.read_digital_D4()
    for i in 0..CONFIG_RETRIES - 1
      begin
        self._set_pin_mode PIN_DIGITAL_D4, PIN_MODE_IN
        return self._read_digital PIN_DIGITAL_D4
      rescue Errno::EREMOTEIO
        next
      end
    end
  end

  def self.read_digital_D5()
    for i in 0..CONFIG_RETRIES - 1
      begin
        self._set_pin_mode PIN_DIGITAL_D5, PIN_MODE_IN
        return self._read_digital PIN_DIGITAL_D5
      rescue Errno::EREMOTEIO
        next
      end
    end
  end

  def self.read_digital_D6()
    for i in 0..CONFIG_RETRIES - 1
      begin
        self._set_pin_mode PIN_DIGITAL_D6, PIN_MODE_IN
        return self._read_digital PIN_DIGITAL_D6
      rescue Errno::EREMOTEIO
        next
      end
    end
  end

  def self.read_digital_D7()
    for i in 0..CONFIG_RETRIES - 1
      begin
        self._set_pin_mode PIN_DIGITAL_D7, PIN_MODE_IN
        return self._read_digital PIN_DIGITAL_D7
      rescue Errno::EREMOTEIO
        next
      end
    end
  end

  def self.read_digital_D8()
    for i in 0..CONFIG_RETRIES - 1
      begin
        self._set_pin_mode PIN_DIGITAL_D8, PIN_MODE_IN
        return self._read_digital PIN_DIGITAL_D8
      rescue Errno::EREMOTEIO
        next
      end
    end
  end

  # Digital write functions.
  def self.write_digital_D2(value)
    for i in 0..CONFIG_RETRIES - 1
      begin
        self._set_pin_mode PIN_DIGITAL_D2, PIN_MODE_OUT
        self._write_digital PIN_DIGITAL_D2, value
        return
      rescue Errno::EREMOTEIO
        next
      end
    end
  end

  def self.write_digital_D3(value)
    for i in 0..CONFIG_RETRIES - 1
      begin
        self._set_pin_mode PIN_DIGITAL_D3, PIN_MODE_OUT
        self._write_digital PIN_DIGITAL_D3, value
        return
      rescue Errno::EREMOTEIO
        next
      end
    end
  end

  def self.write_digital_D4(value)
    for i in 0..CONFIG_RETRIES - 1
      begin
        self._set_pin_mode PIN_DIGITAL_D4, PIN_MODE_OUT
        self._write_digital PIN_DIGITAL_D4, value
        return
      rescue Errno::EREMOTEIO
        next
      end
    end
  end

  def self.write_digital_D5(value)
    for i in 0..CONFIG_RETRIES - 1
      begin
        self._set_pin_mode PIN_DIGITAL_D5, PIN_MODE_OUT
        self._write_digital PIN_DIGITAL_D5, value
        return
      rescue Errno::EREMOTEIO
        next
      end
    end
  end

  def self.write_digital_D6(value)
    for i in 0..CONFIG_RETRIES - 1
      begin
        self._set_pin_mode PIN_DIGITAL_D6, PIN_MODE_OUT
        self._write_digital PIN_DIGITAL_D6, value
        return
      rescue Errno::EREMOTEIO
        next
      end
    end
  end

  def self.write_digital_D7(value)
    for i in 0..CONFIG_RETRIES - 1
      begin
        self._set_pin_mode PIN_DIGITAL_D7, PIN_MODE_OUT
        self._write_digital PIN_DIGITAL_D7, value
        return
      rescue Errno::EREMOTEIO
        next
      end
    end
  end

  def self.write_digital_D8(value)
    for i in 0..CONFIG_RETRIES - 1
      begin
        self._set_pin_mode PIN_DIGITAL_D8, PIN_MODE_OUT
        self._write_digital PIN_DIGITAL_D8, value
        return
      rescue Errno::EREMOTEIO
        next
      end
    end
  end

  # TODO: Implement rest of the commands that are supported by the firmware.

  # Functions for reading and writing I2C slaves connected to
  # I2C-1, I2C-2 or I2C-3 ports of the GrovePi.
  def self.read_grove_pi_i2c(i2c_slave_address, length)
    _ensure_init

    if !@_i2c_slave_addresses.key?(i2c_slave_address)
      path =
        @_i2c_grove_pi.instance_variable_get(:@driver)
                      .instance_variable_get(:@path)

      @_i2c_slave_addresses[i2c_slave_address] = I2CDevice.new address: i2c_slave_address,
                                                               driver: I2CDevice::Driver::I2CDev.new(path)
    end

    bytes = []
    _bytes = @_i2c_slave_addresses[i2c_slave_address].i2cget(i2c_slave_address, length).chars

    for b in _bytes
      bytes << b.ord
    end

    return bytes
  end

  def self.write_grove_pi_i2c(i2c_slave_address, *data)
    _ensure_init

    if !@_i2c_slave_addresses.key?(i2c_slave_address)
      path =
        @_i2c_grove_pi.instance_variable_get(:@driver)
                      .instance_variable_get(:@path)

      @_i2c_slave_addresses[i2c_slave_address] = I2CDevice.new address: i2c_slave_address,
                                                               driver: I2CDevice::Driver::I2CDev.new(path)
    end

    @_i2c_slave_addresses[i2c_slave_address].i2cset i2c_slave_address, *data
  end

  # Miscellaneous functions.
  def self.read_firmware_version()
    for i in 0..CONFIG_RETRIES - 1
      begin
        self._ensure_init
        @_i2c_grove_pi.i2cset @_i2c_grove_pi.address, CMD_READ_FIRMWARE_VERSION, 0, 0, 0
        bytes = @_i2c_grove_pi.i2cget(@_i2c_grove_pi.address, 4).chars
        return [bytes[1].ord, bytes[2].ord, bytes[3].ord]
      rescue Errno::EREMOTEIO
        next
      end
    end
  end
end

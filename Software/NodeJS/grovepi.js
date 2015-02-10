var i2c         = require('i2c')
  , fs          = require('fs')
  , sleep       = require('sleep')
  , bufferTools = require('buffertools').extend()
  , async       = require('async')
  , log         = require('npmlog')
  , cmd         = require('./grovepi.commands')

  , i2c0Path  = '/dev/i2c-0'
  , i2c1Path  = '/dev/i2c-1'
  , bus, device

  , i2cCmd    = 1
  , address   = 0x04
  , bytesLen  = 4
  , trueRet   = 1     // positive value returned by default or in case of success
  , falseRet  = -1    // negative value returned by default (in case of errors)
  , debug     = false

  , initWait  = 1     // in seconds

  , isInit      = false
  , isHalt      = false
  , isBoardBusy = false

var self = module.exports = {
    CELSIUS     : 'c'
  , FAHRENHEIT  : 'f'
  , INPUT       : 'input'
  , OUTPUT      : 'output'
  , DHT_VER     : {
     'DHT11': 0
    , 'DHT22': 1
    , 'DHT21': 2
    , 'AM2301': 3
  },

  init: function(opts) {
    if (typeof opts == 'undefined')
      opts = {}

    if (typeof opts.debug != 'undefined')
      debug = opts.debug

    if (fs.existsSync(i2c0Path)) {
      isHalt = false
      device = i2c0Path
    } else if (fs.existsSync(i2c1Path)) {
      isHalt = false
      device = i2c1Path
    } else {
      var err = new Error('ERROR: GrovePI could not determine your i2c device')
      isHalt = true
      if (typeof opts.onError == 'function') {
        self.utils.debug(err)
        opts.onError(err)
      }
    }

    if (!isHalt) {
      bus = new i2c(address, {
        device: device
      })

      if (!isInit) {
        self.utils.debug('GrovePi is initing')
        sleep.sleep(initWait)
        isInit = true

        if (typeof opts.onInit == 'function') {
          opts.onInit()
        }
      }
    }
  },
  run: function(tasks) {
    async.waterfall(tasks)
  },

  /*
   *
   * Private functions (should not be used directly)
   *
   */
  write_i2c_block: function(block) {
    if (!isInit || isHalt){
      if (!isHalt) {
        self.utils.debug('GrovePi needs to be initialized.')
        return falseRet
      } else {
        return falseRet
      }
    }

    var ret = trueRet
    bus.writeBytes(i2cCmd, block, function(err) {
      isBoardBusy = false

      if (err != null) {
        self.utils.debug(err)
        return falseRet
      }
    })
    return ret
  },

  read_i2c_byte: function() {
    if (!isInit || isHalt){
      if (!isHalt) {
        self.utils.debug('GrovePi needs to be initialized.')
        return falseRet
      } else {
        return falseRet
      }
    }

    return bus.readByte(function(err, res) {
      isBoardBusy = false

      if (err) {
        self.utils.debug(err)
        return falseRet
      } else {
        return res
      }
    })
  },

  read_i2c_block: function(len) {
    if (typeof len == 'undefined')
      len = bytesLen

    if (!isInit || isHalt){
      if (!isHalt) {
        self.utils.debug('GrovePi needs to be initialized.')
        return falseRet
      } else {
        return falseRet
      }
    }

    return bus.readBytes(i2cCmd, len, function(err, res) {
      isBoardBusy = false

      if (err) {
        self.utils.debug(err)
        return falseRet
      } else {
        return res
      }
    })
  },

  /*
   *
   * Basic Arduino Functions
   *
   */
  pinMode: function(pin, mode) {
    if (mode == self.OUTPUT) {
      self.write_i2c_block(cmd.pMode.concat([pin, 1, cmd.unused]))
    } else if (mode == self.INPUT) {
      self.write_i2c_block(cmd.pMode.concat([pin, 0, cmd.unused]))
    }
    isBoardBusy = false
    return trueRet
  },

  digitalRead: function(pin) {
    self.write_i2c_block(cmd.dRead.concat([pin, cmd.unused, cmd.unused]))
    self.utils.wait(100)
    var val = self.read_i2c_byte()
    isBoardBusy = false
    return val
  },

  digitalWrite: function(pin, value) {
    self.write_i2c_block(cmd.dWrite.concat([pin, value, cmd.unused]))
    isBoardBusy = false
    return trueRet
  },

  analogRead: function(pin, callback, len) {
    if (typeof len == 'undefined')
      len = bytesLen

    if (typeof callback != 'function') {
      self.utils.debug('Callback is mandatory')
      return
    }

    if (!isInit || isHalt){
      if (!isHalt) {
        self.utils.debug('GrovePi needs to be initialized.')
        callback(falseRet)
        return
      } else {
        callback(falseRet)
        return
      }
    }

    bus.writeBytes(i2cCmd, cmd.aRead.concat([pin, cmd.unused, cmd.unused]), function onBusRes(err) {
      if (err != null) {
        callback(falseRet)
        isBoardBusy = false
        self.utils.debug(err)
        return
      }

      bus.readByte(function onReadByte(err, res) {
        if (err != null) {
          callback(falseRet)
          isBoardBusy = false
          self.utils.debug(err)
          return
        }

        bus.readBytes(i2cCmd, len, function onReadBytes(err, res) {
          if (err) {
            self.utils.debug(err)
            callback(falseRet)
            isBoardBusy = false
            return falseRet
          }

          callback(res[1] * 256 + res[2])
          isBoardBusy = false
          return trueRet
        })
      })
    })
  },

  analogWrite: function(pin, value) {
    self.write_i2c_block(cmd.aWrite.concat([pin, value, cmd.unused]))
    return trueRet
  },

  /*
   *
   * Grove Specific functions
   *
   */
  version: function(callback) {
    if (isBoardBusy) {
      /*
      self.queue.add({
        'funcName' : 'version',
        'pin'      : -1,
        'args'     : [].slice.call(arguments)
      })
      */
      return self
    }
    isBoardBusy = true

    self.write_i2c_block(cmd.version.concat([cmd.unused, cmd.unused, cmd.unused]))
    self.utils.wait(100)
    self.read_i2c_byte()
    var number = self.read_i2c_block()
    callback(number[1] + '.' + number[2] + '.' + number[3])

    return self
  },

  temp: function(pin, callback) {
    if (isBoardBusy) {
      /*
      self.queue.add({
        'funcName' : 'temp',
        'pin'      : pin,
        'args'     : [].slice.call(arguments)
      })
      */
      return self
    }
    isBoardBusy = true

    self.analogRead(pin, function onTemp(res) {
      var resistance = (1023-a) * 10000 / a
        , number = 1 / (Math.log(resistance / 10000) / 3975 + 1 / 298.15) - 273.15
        
      callback(number)
    })

    return self
  },

  ultrasonicRead: function(pin, callback) {
    if (isBoardBusy) {
      /*
      self.queue.add({
        'funcName' : 'ultrasonicRead',
        'pin'      : pin,
        'args'     : [].slice.call(arguments)
      })
      */
      return self
    }
    isBoardBusy = true

    self.write_i2c_block(cmd.uRead.concat([pin, cmd.unused, cmd.unused]))
    self.utils.wait(200)
    self.read_i2c_byte()
    var number = self.read_i2c_block()
    callback(number[1] * 256 + number[2])

    return self
  },

  acc_xyz: function(callback) {
    if (isBoardBusy) {
      /*
      self.queue.add({
        'funcName' : 'acc_xyz',
        'pin'      : -1,
        'args'     : [].slice.call(arguments)
      })
      */
      return self
    }
    isBoardBusy = true

    self.write_i2c_block(cmd.acc_xyz.concat([cmd.unused, cmd.unused, cmd.unused]))
    self.utils.wait(100)
    self.read_i2c_byte()
    var number = self.read_i2c_block()
    number[1] = number[1] > 32 ? -(number[1]-224) : number[1]
    number[2] = number[2] > 32 ? -(number[2]-224) : number[2]
    number[3] = number[3] > 32 ? -(number[3]-224) : number[3]

    callback([number[1], number[2], number[3]])

    return self
  },

  rtc_getTime: function(callback) {
    if (isBoardBusy) {
      /*
      self.queue.add({
        'funcName' : 'rtc_getTime',
        'pin'      : -1,
        'args'     : [].slice.call(arguments)
      })
      */
      return self
    }
    isBoardBusy = true

    self.write_i2c_block(cmd.rtc_getTime.concat([cmd.unused, cmd.unused, cmd.unused]))
    self.utils.wait(100)
    self.read_i2c_byte()
    var number = self.read_i2c_block()
    callback(number)

    return self
  },

  airQuality: function(pin, callback) {
    if (isBoardBusy) {
      /*
      self.queue.add({
        'funcName' : 'airQuality',
        'pin'      : pin,
        'args'     : [].slice.call(arguments)
      })
      */
      return self
    }
    isBoardBusy = true

    self.pinMode(pin, self.INPUT)
    self.analogRead(pin, function onAirQualityRead(res) {
      var number = parseInt(res)
      callback(number)
    })

    return self
  },

  light: function(pin, callback) {
    if (isBoardBusy) {
      /*
      self.queue.add({
        'funcName' : 'light',
        'pin'      : pin,
        'args'     : [].slice.call(arguments)
      })
      */
      return self
    }
    isBoardBusy = true

    self.pinMode(pin, self.INPUT)
    self.analogRead(pin, function onLightRead(res) {
      var number = parseInt(res)
        , resistance = -1
      if (number <= 0)
        resistance = 0
      else {
        resistance = Number(parseFloat(1023 - number) * 10 / number).toFixed(2)
      }
      callback(resistance)
    })

    return self
  },

  dht: function(pin, moduleType, scale, callback) {
    if (isBoardBusy) {
      /*
      self.queue.add({
        'funcName' : 'dht',
        'pin'      : pin,
        'args'     : [].slice.call(arguments)
      })
      */
      return self
    }
    isBoardBusy = true

    var temp      = null
      , hum       = null
      , heatIndex = null
      

    self.write_i2c_block(cmd.dht_temp.concat([pin, moduleType, cmd.unused]))
    self.utils.wait(500)

    self.read_i2c_byte()
    self.utils.wait(200)

    var number = self.read_i2c_block(9)

    if (number == falseRet) {
      callback(falseRet)
    }

    var tempBuf = number.slice(1,5).reverse()
      , humBuf  = number.slice(5,9).reverse()
      , f = 0
      , h = ''
      

    h = '0x' + tempBuf.toString('hex')
    temp = (h & 0x7fffff | 0x800000) * 1.0 / Math.pow(2,23) * Math.pow(2,  ((h>>23 & 0xff) - 127))
    temp = Number(parseFloat(temp - 0.5).toFixed(2))
    if (scale == self.FAHRENHEIT) {
      temp = self.utils.convertCtoF(temp)
    }

    h = '0x' + humBuf.toString('hex')
    hum = (h & 0x7fffff | 0x800000) * 1.0 / Math.pow(2,23) * Math.pow(2,  ((h>>23 & 0xff) - 127))
    hum = Number(parseFloat(hum - 2).toFixed(2))

    heatIndex = Number(parseFloat(self.utils.computeHeatIndex(temp, hum, scale)).toFixed(2))
    // From: https://github.com/adafruit/DHT-sensor-library/blob/master/DHT.cpp

    callback([temp, hum, heatIndex])

    return self
  },

  ledBar_init: function(pin, orientation, callback) {
    if (isBoardBusy) {
      /*
      self.queue.add({
        'funcName' : 'ledBar_init',
        'pin'      : pin,
        'args'     : [].slice.call(arguments)
      })
      */
      return self
    }
    isBoardBusy = true

    self.write_i2c_block(cmd.ledBarInit.concat([pin, orientation, cmd.unused]))
    callback(self.trueRet)

    return self
  },

  ledBar_orientation: function(pin, orientation, callback) {
    if (isBoardBusy) {
      /*
      self.queue.add({
        'funcName' : 'ledBar_orientation',
        'pin'      : pin,
        'args'     : [].slice.call(arguments)
      })
      */
      return self
    }
    isBoardBusy = true

    self.write_i2c_block(cmd.ledBarInit.concat([pin, orientation, cmd.unused]))
    callback(self.trueRet)

    return self
  },

  ledBar_setLevel: function(pin, level, callback) {
    if (isBoardBusy) {
      /*
      self.queue.add({
        'funcName' : 'ledBar_setLevel',
        'pin'      : pin,
        'args'     : [].slice.call(arguments)
      })
      */
      return self
    }
    isBoardBusy = true

    self.write_i2c_block(cmd.ledBarLevel.concat([pin, level, cmd.unused]))
    callback(self.trueRet)

    return self
  },

  ledBar_setLed: function(pin, led, state, callback) {
    if (isBoardBusy) {
      /*
      self.queue.add({
        'funcName' : 'ledBar_setLed',
        'pin'      : pin,
        'args'     : [].slice.call(arguments)
      })
      */
      return self
    }
    isBoardBusy = true

    self.write_i2c_block(cmd.ledBarSetOne.concat([pin, led, state]))
    callback(self.trueRet)

    return self
  },

  ledBar_toggleLed: function(pin, led, callback) {
    if (isBoardBusy) {
      /*
      self.queue.add({
        'funcName' : 'ledBar_toggleLed',
        'pin'      : pin,
        'args'     : [].slice.call(arguments)
      })
      */
      return self
    }
    isBoardBusy = true

    self.write_i2c_block(cmd.ledBarToggleOne.concat([pin, led, cmd.unused]))
    callback(self.trueRet)

    return self
  },

  ledBar_setBits: function(pin, state, callback) {
    if (isBoardBusy) {
      /*
      self.queue.add({
        'funcName' : 'ledBar_setBits',
        'pin'      : pin,
        'args'     : [].slice.call(arguments)
      })
      */
      return self
    }
    isBoardBusy = true

    var byte1 = state & 255
      , byte2 = state >> 8
      
    self.write_i2c_block(cmd.ledBarSet.concat([pin, byte1, byte2]))
    callback(self.trueRet)

    return self
  },

  ledBar_getBits: function(pin, callback) {
    if (isBoardBusy) {
      /*
      self.queue.add({
        'funcName' : 'ledBar_getBits',
        'pin'      : pin,
        'args'     : [].slice.call(arguments)
      })
      */
      return self
    }
    isBoardBusy = true

    self.write_i2c_block(cmd.ledBarGet.concat([pin, cmd.unused, cmd.unused]))
    self.utils.wait(200)
    self.read_i2c_byte()
    var block = self.read_i2c_block()
    callback(block[1] ^ (block[2]<<8))

    return self
  },

  fourDigit_init: function(pin, callback) {
    if (isBoardBusy) {
      /*
      self.queue.add({
        'funcName' : 'fourDigit_init',
        'pin'      : pin,
        'args'     : [].slice.call(arguments)
      })
      */
      return self
    }
    isBoardBusy = true

    self.write_i2c_block(cmd.fourDigitInit.concat([pin, cmd.unused, cmd.unused]))
    callback(self.trueRet)

    return self
  },

  fourDigit_number: function(pin, value, leadingZero, callback) {
    if (isBoardBusy) {
      /*
      self.queue.add({
        'funcName' : 'fourDigit_number',
        'pin'      : pin,
        'args'     : [].slice.call(arguments)
      })
      */
      return self
    }
    isBoardBusy = true

    // split the value into two bytes so we can render 0000-FFFF on the display
    var byte1 = value & 255
      , byte2 = value >> 8
      
    // separate commands to overcome current 4 bytes per command limitation
    if (leading_zero) {
      self.write_i2c_block(cmd.fourDigitValue.concat([pin, byte1, byte2]))
    } else {
      self.write_i2c_block(cmd.fourDigitValueZeros.concat([pin, byte1, byte2]))
    }
    self.utils.wait(500)
    callback(trueRet)

    return self
  },

  fourDigit_brightness: function(pin, brightness, callback) {
    if (isBoardBusy) {
      /*
      self.queue.add({
        'funcName' : 'fourDigit_brightness',
        'pin'      : pin,
        'args'     : [].slice.call(arguments)
      })
      */
      return self
    }
    isBoardBusy = true

    // not actually visible until next command is executed
    self.write_i2c_block(cmd.fourDigitBrightness.concat([pin, brightness, cmd.unused]))
    self.utils.wait(500)
    callback(trueRet)

    return self
  },

  fourDigit_digit: function(pin, segment, value, callback) {
    if (isBoardBusy) {
      /*
      self.queue.add({
        'funcName' : 'fourDigit_digit',
        'pin'      : pin,
        'args'     : [].slice.call(arguments)
      })
      */
      return self
    }
    isBoardBusy = true

    self.write_i2c_block(cmd.fourDigitIndividualDigit.concat([pin, segment, value]))
    self.utils.wait(500)
    callback(trueRet)

    return self
  },

  fourDigit_segment: function(pin, segment, leds, callback) {
    if (isBoardBusy) {
      /*
      self.queue.add({
        'funcName' : 'fourDigit_segment',
        'pin'      : pin,
        'args'     : [].slice.call(arguments)
      })
      */
      return self
    }
    isBoardBusy = true

    self.write_i2c_block(cmd.fourDigitIndividualLeds.concat([pin, segment, leds]))
    self.utils.wait(500)
    callback(trueRet)

    return self
  },

  fourDigit_score: function(pin, left, right, callback) {
    if (isBoardBusy) {
      /*
      self.queue.add({
        'funcName' : 'fourDigit_score',
        'pin'      : pin,
        'args'     : [].slice.call(arguments)
      })
      */
      return self
    }
    isBoardBusy = true

    self.write_i2c_block(cmd.fourDigitScore.concat([pin, left, right]))
    self.utils.wait(500)
    callback(trueRet)

    return self
  },

  fourDigit_monitor: function(pin, analog, duration, callback) {
    if (isBoardBusy) {
      /*
      self.queue.add({
        'funcName' : 'fourDigit_monitor',
        'pin'      : pin,
        'args'     : [].slice.call(arguments)
      })
      */
      return self
    }
    isBoardBusy = true

    self.write_i2c_block(cmd.fourDigitAnalogRead.concat([pin, analog, duration]))
    self.utils.wait(duration/1000 + 500) // TODO: This should be tested
    callback(trueRet)

    return self
  },

  fourDigit_on: function(pin, callback) {
    if (isBoardBusy) {
      /*
      self.queue.add({
        'funcName' : 'fourDigit_on',
        'pin'      : pin,
        'args'     : [].slice.call(arguments)
      })
      */
      return self
    }
    isBoardBusy = true

    self.write_i2c_block(cmd.fourDigitAllOn.concat([pin, cmd.unused, cmd.unused]))
    self.utils.wait(500)
    callback(trueRet)

    return self
  },

  fourDigit_off: function(pin, callback) {
    if (isBoardBusy) {
      /*
      self.queue.add({
        'funcName' : 'fourDigit_off',
        'pin'      : pin,
        'args'     : [].slice.call(arguments)
      })
      */
      return self
    }
    isBoardBusy = true

    self.write_i2c_block(cmd.fourDigitAllOff.concat([pin, cmd.unused, cmd.unused]))
    self.utils.wait(500)
    callback(trueRet)

    return self
  },

  storeColor: function(red, green, blue, callback) {
    if (isBoardBusy) {
      /*
      self.queue.add({
        'funcName' : 'storeColor',
        'pin'      : -1,
        'args'     : [].slice.call(arguments)
      })
      */
      return self
    }
    isBoardBusy = true

    self.write_i2c_block(cmd.storeColor.concat([red, green, blue]))
    self.utils.wait(500)
    callback(trueRet)

    return self
  },

  chainableRgbLed_init: function(pin, numLeds, callback) {
    if (isBoardBusy) {
      /*
      self.queue.add({
        'funcName' : 'chainableRgbLed_init',
        'pin'      : pin,
        'args'     : [].slice.call(arguments)
      })
      */
      return self
    }
    isBoardBusy = true

    self.write_i2c_block(cmd.chainableRgbLedInit.concat([pin, numLeds, cmd.unused]))
    self.utils.wait(500)
    callback(trueRet)

    return self
  },

  chainableRgbLed_test: function(pin, numLeds, testColor, callback) {
    if (isBoardBusy) {
      /*
      self.queue.add({
        'funcName' : 'chainableRgbLed_test',
        'pin'      : pin,
        'args'     : [].slice.call(arguments)
      })
      */
      return self
    }
    isBoardBusy = true

    self.write_i2c_block(cmd.chainableRgbLedTest.concat([pin, numLeds, testColor]))
    self.utils.wait(500)
    callback(trueRet)

    return self
  },

  chainableRgbLed_pattern: function(pin, pattern, whichLed, callback) {
    if (isBoardBusy) {
      /*
      self.queue.add({
        'funcName' : 'chainableRgbLed_pattern',
        'pin'      : pin,
        'args'     : [].slice.call(arguments)
      })
      */
      return self
    }
    isBoardBusy = true

    self.write_i2c_block(cmd.chainableRgbLedSetPattern.concat([pin, pattern, whichLed]))
    self.utils.wait(500)
    callback(trueRet)

    return self
  },

  chainableRgbLed_modulo: function(pin, offset, divisor, callback) {
    if (isBoardBusy) {
      /*
      self.queue.add({
        'funcName' : 'chainableRgbLed_modulo',
        'pin'      : pin,
        'args'     : [].slice.call(arguments)
      })
      */
      return self
    }
    isBoardBusy = true

    self.write_i2c_block(cmd.chainableRgbLedSetModulo.concat([pin, offset, divisor]))
    self.utils.wait(500)
    callback(trueRet)

    return self
  },

  chainableRgbLed_setLevel: function(pin, level, reverse, callback) {
    if (isBoardBusy) {
      /*
      self.queue.add({
        'funcName' : 'chainableRgbLed_setLevel',
        'pin'      : pin,
        'args'     : [].slice.call(arguments)
      })
      */
      return self
    }
    isBoardBusy = true

    self.write_i2c_block(cmd.chainableRgbLedSetLevel.concat([pin, level, reverse]))
    self.utils.wait(500)
    callback(trueRet)

    return self
  },

  /*
   *
   * Utils functions
   *
   */
  utils: {
    debug: function(msg) {
      if (debug) 
        log.info(arguments.callee.caller.name, msg)
    },
    wait: function(ms) {
      sleep.usleep(1000 * ms)
    },
    convertCtoF: function(temp) {
      return temp * 9 / 5 + 32
    },
    convertFtoC: function(temp) {
      return (temp - 32) * 5 / 9
    },
    computeHeatIndex: function(temp, hum, scale) {
      // http://www.hpc.ncep.noaa.gov/html/heatindex_equation.shtml

      if (typeof scale == 'undefined' || scale == self.CELSIUS) {
        temp = self.utils.convertCtoF(temp)
      }

      return  -42.379 +
               2.04901523  * temp +
               10.14333127 * hum +
              -0.22475541  * temp * hum +
              -0.00683783  * Math.pow(temp, 2) +
              -0.05481717  * Math.pow(hum, 2) +
               0.00122874  * Math.pow(temp, 2) * hum +
               0.00085282  * temp * Math.pow(hum, 2) +
              -0.00000199  * Math.pow(temp, 2) * Math.pow(hum, 2)
    }
  }
}

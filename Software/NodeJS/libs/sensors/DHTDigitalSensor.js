var DigitalSensor = require('./base/digitalSensor')
var commands     = require('../commands')

function DHTDigitalSensor(pin, moduleType, scale) {
  DigitalSensor.apply(this, Array.prototype.slice.call(arguments))
  this.moduleType = moduleType
  this.scale = scale
}
function convertCtoF(temp) {
  return temp * 9 / 5 + 32
}
function convertFtoC(temp) {
  return (temp - 32) * 5 / 9
}
function getHeatIndex(temp, hum, scale) {
  // http://www.hpc.ncep.noaa.gov/html/heatindex_equation.shtml
  if (typeof scale == 'undefined' || scale == this.CELSIUS) {
    temp = convertCtoF(temp)
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

DHTDigitalSensor.prototype = new DigitalSensor()
DHTDigitalSensor.VERSION = {
    'DHT11' : 0
  , 'DHT22' : 1
  , 'DHT21' : 2
  , 'AM2301': 3
}
DHTDigitalSensor.CELSIUS = 'c'
DHTDigitalSensor.FAHRENHEIT = 'f'

DHTDigitalSensor.prototype.read = function() {
  var write = this.board.writeBytes(commands.dht_temp.concat([this.pin, this.moduleType, commands.unused]))
  if (write) {
    this.board.wait(500)
    this.board.readByte()
    this.board.wait(200)
    var bytes = this.board.readBytes(9)
    if (bytes instanceof Buffer) {
      var hex
      var tempBytes = bytes.slice(1, 5).reverse()
      var humBytes = bytes.slice(5, 9).reverse()

      hex = '0x' + tempBytes.toString('hex')
      var temp = (hex & 0x7fffff | 0x800000) * 1.0 / Math.pow(2, 23) * Math.pow(2, ((hex >> 23 & 0xff) - 127))
      temp = +(Number(parseFloat(temp - 0.5).toFixed(2)))
      if (this.scale == this.FAHRENHEIT) {
        temp = convertCtoF(temp)
      }

      hex = '0x' + humBytes.toString('hex')
      var hum = (hex & 0x7fffff | 0x800000) * 1.0 / Math.pow(2, 23) * Math.pow(2, ((hex >> 23 & 0xff) - 127))
      hum = +(Number(parseFloat(hum - 2).toFixed(2)))

      var heatIndex = +(Number(parseFloat(getHeatIndex(temp, hum, this.scale)).toFixed(2)))
      // From: https://github.com/adafruit/DHT-sensor-library/blob/master/DHT.cpp

      return [temp, hum, heatIndex]
    } else
      return false
  } else {
    return false
  }
}

module.exports = DHTDigitalSensor
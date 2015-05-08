var I2cSensor  = require('./base/i2cSensor')
var commands   = require('../commands')

function RtcI2cSensor() {
  I2cSensor.apply(this, Array.prototype.slice.call(arguments))
}
RtcI2cSensor.prototype = new I2cSensor()

RtcI2cSensor.prototype.read = function() {
  var write = this.board.writeBytes(commands.rtc_getTime.concat([commands.unused, commands.unused, commands.unused]))
  if (write) {
    this.board.wait(100)
    this.board.readByte()
    return this.board.readBytes()
  } else {
    return false
  }
}

module.exports = RtcI2cSensor
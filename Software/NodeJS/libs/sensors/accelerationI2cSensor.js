var util       = require('util')
var I2cSensor  = require('./base/i2cSensor')
var commands   = require('../commands')

function AccelerationI2cSensor() {
  I2cSensor.apply(this, Array.prototype.slice.call(arguments))
}
AccelerationI2cSensor.prototype = new I2cSensor()

AccelerationI2cSensor.prototype.read = function() {
  var write = this.board.writeBytes(commands.acc_xyz.concat([commands.unused, commands.unused, commands.unused]))
  if (write) {
    this.board.wait(100)
    this.board.readByte()
    var bytes = this.board.readBytes()
    if (bytes instanceof Buffer) {
      var x = bytes[1] > 32 ? -(bytes[1]-224) : bytes[1]
      var y = bytes[2] > 32 ? -(bytes[2]-224) : bytes[2]
      var z = bytes[3] > 32 ? -(bytes[3]-224) : bytes[3]
      return [x, y, z]
    } else {
      return false
    }
  } else {
    return false
  }
}

module.exports = AccelerationI2cSensor
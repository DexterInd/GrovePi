// TODO: call disable function on exit
var DigitalSensor = require('./base/digitalSensor')
var commands     = require('../commands')

function DustDigitalSensor(pin) {
  DigitalSensor.apply(this, Array.prototype.slice.call(arguments))
}
DustDigitalSensor.prototype = new DigitalSensor()

DustDigitalSensor.prototype.read = function() {
  var write = this.board.writeBytes(commands.dustSensorRead.concat([this.pin, commands.unused, commands.unused]))
  if (write) {
    this.board.wait(200)
    this.board.readByte()
    var bytes = this.board.readBytes()
    if (bytes instanceof Buffer && bytes[1] != 255)
      return [bytes[1], (bytes[4] * 256 * 256 + bytes[3] * 256 + bytes[2])]
    else
      return false
  } else {
    return false
  }
}
DustDigitalSensor.prototype.enable = function() {
  var write = this.board.writeBytes(commands.dustSensorEn.concat([commands.unused, commands.unused, commands.unused]))
  if (write) {
    this.board.wait(200)
    return true
  } else {
    return false
  }
}
DustDigitalSensor.prototype.disable = function() {
  var write = this.board.writeBytes(commands.dustSensorDis.concat([commands.unused, commands.unused, commands.unused]))
  if (write) {
    this.board.wait(200)
    return true
  } else {
    return false
  }
}

module.exports = DustDigitalSensor
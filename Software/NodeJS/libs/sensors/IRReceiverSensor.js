var util         = require('util')
var Sensor       = require('./base/sensor')
var commands     = require('../commands')

function IRReceiverSensor(pin) {
  pin += 1
  Sensor.apply(this, Array.prototype.slice.call(arguments))
  this.pin = pin
}
util.inherits(IRReceiverSensor, Sensor);
IRReceiverSensor.prototype = new DigitalSensor()

IRReceiverSensor.prototype.read = function() {
  this.write(commands.unused)
  var writeRet = this.board.writeBytes(commands.irRead.concat([commands.unused, commands.unused, commands.unused]))
  if (writeRet) {
    this.board.readByte()
    var bytes = this.board.readBytes(22)
    if (bytes instanceof Buffer && bytes[1] != 255) {
      bytes.slice(0,1)
      return bytes
    } else {
      return false
    }
  } else {
    return false
  }
}
IRReceiverSensor.prototype.write = function(value) {
  return this.board.writeBytes(commands.irRecvPin.concat([this.pin, value, commands.unused]))
}

module.exports = DigitalSensor
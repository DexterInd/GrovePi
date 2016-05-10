// TODO: call disable function on exit
var DigitalSensor = require('./base/digitalSensor')
var commands     = require('../commands')

function WaterFlowDigitalSensor(pin) {
  DigitalSensor.apply(this, Array.prototype.slice.call(arguments))
}
WaterFlowDigitalSensor.prototype = new DigitalSensor()

WaterFlowDigitalSensor.prototype.read = function() {
  var write = this.board.writeBytes(commands.flowRead.concat([this.pin, commands.unused, commands.unused]))
  if (write) {
    this.board.wait(200)
    this.board.readByte()
    var bytes = this.board.readBytes()
    if (bytes instanceof Buffer && bytes[1] != 255)
      return [bytes[1], (bytes[3] * 256 + bytes[2])]
    else
      return false
  } else {
    return false
  }
}
WaterFlowDigitalSensor.prototype.enable = function() {
  var write = this.board.writeBytes(commands.flowEn.concat([commands.unused, commands.unused, commands.unused]))
  if (write) {
    this.board.wait(200)
    return true
  } else {
    return false
  }
}
WaterFlowDigitalSensor.prototype.disable = function() {
  var write = this.board.writeBytes(commands.flowDis.concat([commands.unused, commands.unused, commands.unused]))
  if (write) {
    this.board.wait(200)
    return true
  } else {
    return false
  }
}

module.exports = WaterFlowDigitalSensor
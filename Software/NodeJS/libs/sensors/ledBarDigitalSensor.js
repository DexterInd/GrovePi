var DigitalSensor = require('./base/digitalSensor')
var commands     = require('../commands')

function LedBarDigitalSensor(pin, orientation) {
  DigitalSensor.apply(this, Array.prototype.slice.call(arguments))
  this.orientation = orientation
  this.level = 0
}
LedBarDigitalSensor.prototype = new DigitalSensor()

LedBarDigitalSensor.prototype.init = function() {
  return this.setOrientation(this.orientation)
}
LedBarDigitalSensor.prototype.setOrientation = function(orientation) {
  this.board.pinMode(this.board.OUTPUT)
  this.orientation = orientation
  return this.board.writeBytes(commands.ledBarInit.concat([this.pin, this.orientation, commands.unused]))
}
LedBarDigitalSensor.prototype.setLevel = function(level) {
  this.board.pinMode(this.board.OUTPUT)
  this.level = level
  return this.board.writeBytes(commands.ledBarLevel.concat([this.pin, this.level, commands.unused]))
}
LedBarDigitalSensor.prototype.setLed = function(led, state) {
  this.board.pinMode(this.board.OUTPUT)
  return this.board.writeBytes(commands.ledBarSetOne.concat([this.pin, led, state]))
}
LedBarDigitalSensor.prototype.toggleLed = function(led) {
  this.board.pinMode(this.board.OUTPUT)
  return this.board.writeBytes(commands.ledBarToggleOne.concat([this.pin, led, commands.unused]))
}
LedBarDigitalSensor.prototype.setBits = function(led, state) {
  this.board.pinMode(this.board.OUTPUT)
  var byte1 = state & 255
  var byte2 = state >> 8
  return this.board.writeBytes(commands.ledBarSet.concat([this.pin, byte1, byte2]))
}
LedBarDigitalSensor.prototype.getBits = function() {
  this.board.pinMode(this.board.OUTPUT)
  var byte1 = state & 255
  var byte2 = state >> 8
  var write = this.board.writeBytes(commands.ledBarGet.concat([this.pin, commands.unused, commands.unused]))
  if (write) {
    this.board.wait(200)
    this.board.readByte()
    var bytes = this.board.readBytes()
    if (bytes instanceof Buffer)
      return (bytes[1] ^ (bytes[2] << 8))
    else
      return false
  } else {
    return false
  }
}

module.exports = LedBarDigitalSensor
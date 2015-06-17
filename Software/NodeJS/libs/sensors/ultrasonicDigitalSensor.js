var DigitalSensor = require('./base/digitalSensor')
var commands     = require('../commands')

function UltrasonicDigitalSensor(pin) {
  DigitalSensor.apply(this, Array.prototype.slice.call(arguments))
}
UltrasonicDigitalSensor.prototype = new DigitalSensor()

UltrasonicDigitalSensor.prototype.read = function() {
  var write = this.board.writeBytes(commands.uRead.concat([this.pin, commands.unused, commands.unused]))
  if (write) {
    this.board.wait(200)
    this.board.readByte()
    var bytes = this.board.readBytes()
    if (bytes instanceof Buffer)
      return (bytes[1] * 256 + bytes[2])
    else
      return false
  } else {
    return false
  }
}

module.exports = UltrasonicDigitalSensor
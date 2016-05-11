var GrovePi = require('../libs').GrovePi
var Commands = GrovePi.commands
var Board = GrovePi.board
var AccelerationI2cSensor = GrovePi.sensors.AccelerationI2C
var UltrasonicDigitalSensor = GrovePi.sensors.UltrasonicDigital
var AirQualityAnalogSensor = GrovePi.sensors.AirQualityAnalog
var DHTDigitalSensor = GrovePi.sensors.DHTDigital
var LightAnalogSensor = GrovePi.sensors.LightAnalog

var board

function start() {
  console.log('starting')

  board = new Board({
    debug: true,
    onError: function(err) {
      console.log('TEST ERROR')
      console.log(err)
    },
    onInit: function(res) {
      if (res) {
        var accSensor = new AccelerationI2cSensor()
        // I2C sensor doesn't need to specify a port
        var ultrasonicSensor = new UltrasonicDigitalSensor(4)
        // Digital Port 4
        var airQualitySensor = new AirQualityAnalogSensor(1)
        // Analog Port 1
        var dhtSensor = new DHTDigitalSensor(3, DHTDigitalSensor.VERSION.DHT22, DHTDigitalSensor.CELSIUS)
        // Digital Port 3
        var lightSensor = new LightAnalogSensor(2)
        // Analog Port 2

        console.log('GrovePi Version :: ' + board.version())

        // Acc. XYZ
        console.log('Acceleration I2C Sensor (single read) :: ' + accSensor.read())
        console.log('Acceleration I2C Sensor (start stream - 1sec delay)')
        accSensor.stream(1000, function(res) {
          console.log('Acceleration stream value=' + res)
        })
        console.log('Acceleration I2C Sensor (start watch)')
        accSensor.on('change', function(res) {
          console.log('Acceleration onChange value=' + res)
        })
        accSensor.watch()

        // Ultrasonic Ranger
        console.log('Ultrasonic Ranger Digital Sensor (start watch)')
        ultrasonicSensor.on('change', function(res) {
          console.log('Ultrasonic Ranger onChange value=' + res)
        })
        //ultrasonicSensor.watch()

        // Air Quality Sensor
        console.log('AirQuality Analog Sensor (start watch)')
        airQualitySensor.on('change', function(res) {
          console.log('AirQuality onChange value=' + res)
        })
        airQualitySensor.watch()

        // DHT Sensor
        console.log('DHT Digital Sensor (start watch)')
        dhtSensor.on('change', function(res) {
          console.log('DHT onChange value=' + res)
        })
        dhtSensor.watch(500) // milliseconds

        // Light Sensor
        console.log('Light Analog Sensor (start watch)')
        lightSensor.on('change', function(res) {
          console.log('Light onChange value=' + res)
        })
        lightSensor.watch()

        // Custom external reading
        console.log('Custom external reading')
        console.log('customAccelerationReading()::' + customAccelerationReading())
      } else {
        console.log('TEST CANNOT START')
      }
    }
  })
  board.init()
}

function customAccelerationReading() {
  var write = board.writeBytes(Commands.acc_xyz.concat([Commands.unused, Commands.unused, Commands.unused]))
  if (write) {
    board.wait(100)
    board.readByte()
    var bytes = board.readBytes()
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

function onExit(err) {
  console.log('ending')
  board.close()
  process.removeAllListeners()
  process.exit()
  if (typeof err != 'undefined')
    console.log(err)
}

// starts the test
start()
// catches ctrl+c event
process.on('SIGINT', onExit)

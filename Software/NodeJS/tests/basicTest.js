var GrovePi = require('../libs').GrovePi
var Commands = GrovePi.commands
var Board = GrovePi.board
var AccelerationI2cSensor = GrovePi.sensors.AccelerationI2C
var UltrasonicDigitalSensor = GrovePi.sensors.UltrasonicDigital
var AirQualityAnalogSensor = GrovePi.sensors.AirQualityAnalog
var DHTDigitalSensor = GrovePi.sensors.DHTDigital
var LightAnalogSensor = GrovePi.sensors.LightAnalog
var DigitalButtonSensor = GrovePi.sensors.DigitalButton
var LoudnessAnalogSensor = GrovePi.sensors.LoudnessAnalog
var RotaryAngleAnalogSensor = GrovePi.sensors.RotaryAnalog
var DustDigitalSensor = GrovePi.sensors.dustDigital

var board


var testOptions = {
  acceleration: false,
  ultrasonic: false,
  airQuality: false,
  dhtDigital: false,
  lightAnalog: false,
  digitalButton: true,
  loudnessAnalog: false,
  rotaryAngle: true,
  dust: true,
  customAccelerationReading: false
}

function start() {
  console.log('starting')

  board = new Board({
    debug: true,
    onError: function (err) {
      console.log('TEST ERROR')
      console.log(err)
    },
    onInit: function (res) {
      if (res) {

        console.log('GrovePi Version :: ' + board.version())

        if (testOptions.acceleration) {
          var accSensor = new AccelerationI2cSensor()
          // I2C sensor doesn't need to specify a port
          // Acc. XYZ
          console.log('Acceleration I2C Sensor (single read) :: ' + accSensor.read())
          console.log('Acceleration I2C Sensor (start stream - 1sec delay)')
          accSensor.stream(1000, function (res) {
            console.log('Acceleration stream value=' + res)
          })
          console.log('Acceleration I2C Sensor (start watch)')
          accSensor.on('change', function (res) {
            console.log('Acceleration onChange value=' + res)
          })
          accSensor.watch()
        }

        if (testOptions.ultrasonic) {
          var ultrasonicSensor = new UltrasonicDigitalSensor(3)
          // Digital Port 3
          // Ultrasonic Ranger
          console.log('Ultrasonic Ranger Digital Sensor (start watch)')
          ultrasonicSensor.on('change', function (res) {
            console.log('Ultrasonic Ranger onChange value=' + res)
          })
          ultrasonicSensor.watch()
        }

        if (testOptions.airQuality) {
          var airQualitySensor = new AirQualityAnalogSensor(1)
          // Analog Port 1
          // Air Quality Sensor
          console.log('AirQuality Analog Sensor (start watch)')
          airQualitySensor.on('change', function (res) {
            console.log('AirQuality onChange value=' + res)
          })
          airQualitySensor.watch()
        }

        if (testOptions.dhtDigital) {
          var dhtSensor = new DHTDigitalSensor(3, DHTDigitalSensor.VERSION.DHT22, DHTDigitalSensor.CELSIUS)
          // Digital Port 3
          // DHT Sensor
          console.log('DHT Digital Sensor (start watch)')
          dhtSensor.on('change', function (res) {
            console.log('DHT onChange value=' + res)
          })
          dhtSensor.watch(500) // milliseconds
        }

        if (testOptions.lightAnalog) {
          var lightSensor = new LightAnalogSensor(3)
          // Analog Port 3
          // Light Sensor
          console.log('Light Analog Sensor (start watch)')
          lightSensor.on('change', function (res) {
            console.log('Light onChange value=' + res)
          })
          lightSensor.watch()
        }

        if (testOptions.loudnessAnalog) {
          var loudnessSensor = new LoudnessAnalogSensor(2)
          //Analog Port 2
          // Loudness Sensor
          console.log('Loudness Analog Sensor (start monitoring - reporting results every 10s)')
          loudnessSensor.start()
          setInterval(loudnessSensorGetAvgMax, 10000, loudnessSensor)
        }

        if (testOptions.digitalButton) {
          var buttonSensor = new DigitalButtonSensor(4)
          //Digital Port 4
          // Button sensor
          console.log('Digital Button Sensor (start watch)')
          buttonSensor.on('down', function (res) {
            //res will be either singlepress or longpress
            console.log('Button onDown, data=' + res)
          })
          buttonSensor.watch()
        }

        if (testOptions.rotaryAngle) {
          var rotaryAngleSensor = new RotaryAngleAnalogSensor(1)
          //Analog Port 1
          // Rotary Angle Sensor
          console.log('Rotary Angle Sensor (start watch)')
          rotaryAngleSensor.start()
          rotaryAngleSensor.on('data', function (res) {
            console.log('Rotary onData value=' + res)
          })
        }

        if (testOptions.dust) {
          var dustSensor = new DustDigitalSensor(2)
          //digital port 2
          // Dust Digital Sensor
          console.log('Dust Digital Sensor (start monitoring - reporting results every 30s)')
          //we must get results every 30 seconds
          dustSensor.start()
          setInterval(dustSensorGetAvgMax, 30 * 1000, dustSensor)
        }

        if (testOptions.customAccelerationReading) {
          // Custom external reading
          console.log('Custom external reading')
          console.log('customAccelerationReading()::' + customAccelerationReading())
        }
      } else {
        console.log('TEST CANNOT START')
      }
    }
  })
  board.init()
}

function loudnessSensorGetAvgMax(loudnessSensor) {
  var res = loudnessSensor.readAvgMax()
  console.log('Loudness avg value=' + res.avg + ' and max value=' + res.max)
}

function dustSensorGetAvgMax(dustSensor) {
  var res = dustSensor.readAvgMax()
  //avg and max will be the same in this test
  //since we're gathering them over 30 seconds
  //but that's the same pediod this loop runs
  console.log('Dust avg value=' + res.avg + ' and max value=' + res.max)
}

function customAccelerationReading() {
  var write = board.writeBytes(Commands.acc_xyz.concat([Commands.unused, Commands.unused, Commands.unused]))
  if (write) {
    board.wait(100)
    board.readByte()
    var bytes = board.readBytes()
    if (bytes instanceof Buffer) {
      var x = bytes[1] > 32 ? -(bytes[1] - 224) : bytes[1]
      var y = bytes[2] > 32 ? -(bytes[2] - 224) : bytes[2]
      var z = bytes[3] > 32 ? -(bytes[3] - 224) : bytes[3]
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
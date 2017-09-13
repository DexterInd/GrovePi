var AnalogSensor = require('./base/analogSensor')
var helpers = require('./helpers')
const FULL_ANGLE = 300

//RotaryAngleSensor
//returns a value from 0 to 100
//implemented a basic noise filtering algorithm, as in our experiments
//the rotary sensor was throwing random values at random times
function RotaryAngleAnalogSensor(pin, watchDelay, samplesize) {
    AnalogSensor.apply(this, Array.prototype.slice.call(arguments))
    this.watchDelay = watchDelay || 10
    this.samplesize = samplesize || 40
    //watchDelay * samplesize equals the miliseconds interval that the sensor will report data
}
RotaryAngleAnalogSensor.prototype = new AnalogSensor()

RotaryAngleAnalogSensor.prototype.read = function () {
    let value = AnalogSensor.prototype.read.call(this)
    
    let degrees = convertDHTToDegrees(value)

    //Calculate result (0 to 100) from degrees(0 to 300)
    let result = Math.floor(degrees / FULL_ANGLE * 100)

    return result
}

const convertDHTToDegrees = function (value) {
    //http://wiki.seeed.cc/Grove-Rotary_Angle_Sensor/
    let adc_ref = 5
    let grove_vcc = 5
  
    let voltage = helpers.round((value) * adc_ref / 1023, 2)

    //Calculate rotation in degrees(0 to 300)
    return helpers.round((voltage * FULL_ANGLE) / grove_vcc, 2)
}

RotaryAngleAnalogSensor.prototype.start = function () {
    setInterval(loop.bind(this), this.watchDelay)
}

RotaryAngleAnalogSensor.prototype.stop = function () {
    clearInterval(loop)
}

//new array initialized to zero
let temp = Array.apply(null, Array(101)).map(Number.prototype.valueOf, 0) //0..100
let timesRun = 0

let previousData = null

function loop() {
    const reading = this.read()
    if (reading < 0 || reading > 100) throw new Error('improper reading')

    temp[reading]++
    if (++timesRun === this.samplesize) {
        //find the index of the biggest integer
        const result = temp.indexOf(Math.max(...temp))
        timesRun = 0
        //reset the array
        temp = Array.apply(null, Array(101)).map(Number.prototype.valueOf, 0)
        
        //compare current data to previous data
        if (previousData === null || Math.abs(result - previousData) != 0) {
            //there is a new value
            this.emit('data', result)
            previousData = result
        }
    }
}

module.exports = RotaryAngleAnalogSensor
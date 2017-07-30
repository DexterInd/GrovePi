var AnalogSensor = require('./base/analogSensor')

//same class can be used for the sound sensor
function LoudnessAnalogSensor(pin, samplespersecond) {
    AnalogSensor.apply(this, Array.prototype.slice.call(arguments))
    this.samplespersecond = samplespersecond || 5
    this.results = new Array()
}
LoudnessAnalogSensor.prototype = new AnalogSensor()

//returns loudness average and max for values taken since the last time it was called
LoudnessAnalogSensor.prototype.readAvgMax = function () {
    if (this.results.length == 0)
        throw new Error('no results. Did you call start()?')

    //reduce values to get the sum
    let sum = this.results.reduce((acc, cur) => acc + cur, 0)
    let avg = sum / this.results.length

    //reduce the values to get the max
    let max = this.results.reduce(function (a, b) {
        return Math.max(a, b)
    })

    //reset the array - clear its elements
    this.results = new Array()

    return {
        avg,
        max
    }
}

LoudnessAnalogSensor.prototype.start = function () {
    loop.bind(this)() //so we can use 'this' inside the loop method
    setInterval(loop.bind(this), 1000 / this.samplespersecond)
}

LoudnessAnalogSensor.prototype.stop = function () {
    clearInterval(loop)
}

function loop() {
    let currentResult = this.read()
    this.results.push(currentResult)
}

module.exports = LoudnessAnalogSensor
var DigitalInput = require('./base/digitalSensor')

const buttonMode = {
    UP: 0,
    DOWN: 1
}

var mode = buttonMode.UP //not pressed

var pressedDateTime
var currentDateTime
var milliseconds

//digital button, can throw singlepress and longpress events
function DigitalButton(pin, longPressDelay) {
    DigitalInput.apply(this, Array.prototype.slice.call(arguments))
    this.longPressDelay = longPressDelay || 1100
    this.on('change', function (res) {
        //user presses the button for the first time
        if (res == 1 && mode === buttonMode.UP) {
            pressedDateTime = new Date()
            mode = buttonMode.DOWN
            return
        }
        //user continues to press the button
        else if (res == 1 && mode === buttonMode.DOWN) {
            //do nothing
            return
        } else { //res == 0 so user has lifted her finger
            currentDateTime = new Date()
            milliseconds = currentDateTime.getTime() - pressedDateTime.getTime()
            //if less than longPressDelay milliseconds
            if (milliseconds <= this.longPressDelay) {
                this.emit('down', 'singlepress')
            } else {
                this.emit('down', 'longpress')
            }
            //reset the mode
            mode = buttonMode.UP
        }
    });
}

DigitalButton.prototype = new DigitalInput()

module.exports = DigitalButton

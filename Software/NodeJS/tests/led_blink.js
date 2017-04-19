var GrovePi = require('../libs').GrovePi

// put led in port D3 
var led = new GrovePi.sensors.DigitalOutput(3);

// status will tell us if the led is on or off
var status = 0;

var board;

function toggle() {

    if (status == 0){
        console.log("toggle off");
        led.turnOff();
        status = 1;
    }
    else {
        console.log("toggle on");
        led.turnOn();
        status = 0;
    }
}

function start() {
  console.log('starting')

  board = new GrovePi.board({
    debug: true,
    onError: function(err) {
      console.log('TEST ERROR')
    },
      
    onInit: function(res) {
        console.log("OnInit");
        if (res) {
            // call toggle every second
            setInterval(toggle, 1000)
        }
    }
  })

  board.init();
} // end start()
 

// called on Ctrl-C. 
// close the board and clean up 
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


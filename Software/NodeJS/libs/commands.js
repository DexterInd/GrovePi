module.exports = {
  //Command Format
  // digitalRead() command format header
    dRead                                       : [1]
  // digitalWrite() command format header
  , dWrite                                      : [2]
  // analogRead() command format header
  , aRead                                       : [3]
  // analogWrite() command format header
  , aWrite                                      : [4]
  // pinMode() command format header
  , pMode                                       : [5]
  // Ultrasonic read
  , uRead                                       : [7]
  // Get firmware version
  , version                                     : [8]
  // Accelerometer (+/- 1.5g) read
  , acc_xyz                                     : [20]
  // RTC get time
  , rtc_getTime                                 : [30]
  // DHT Pro sensor temperature
  , dht_temp                                    : [40]

  // Grove LED Bar commands
  // Initialise
  , ledBarInit                                  : [50]
  // Set orientation
  , ledBarOrient                                : [51]
  // Set level
  , ledBarLevel                                 : [52]
  // Set single LED
  , ledBarSetOne                                : [53]
  // Toggle single LED
  , ledBarToggleOne                             : [54]
  // Set all LEDs
  , ledBarSet                                   : [55]
  // Get current state
  , ledBarGet                                   : [56]

  // Grove 4 Digit Display commands
  // Initialise
  , fourDigitInit                               : [70]
  // Set brightness, not visible until next cmd
  , fourDigitBrightness                         : [71]
  // Set numeric value without leading zeros
  , fourDigitValue                              : [72]
  // Set numeric value with leading zeros
  , fourDigitValueZeros                         : [73]
  // Set individual digit
  , fourDigitIndividualDigit                    : [74]
  // Set individual leds of a segment
  , fourDigitIndividualLeds                     : [75]
  // Set left and right values with colon
  , fourDigitScore                              : [76]
  // Analog read for n seconds
  , fourDigitAnalogRead                         : [77]
  // Entire display on
  , fourDigitAllOn                              : [78]
  // Entire display off
  , fourDigitAllOff                             : [79]

  // Grove Chainable RGB LED commands
  // Store color for later use
  , storeColor                                  : [90]
  // Initialise
  , chainableRgbLedInit                         : [91]
  // Initialise and test with a simple color
  , chainableRgbLedTest                         : [92]
  // Set one or more leds to the stored color by pattern
  , chainableRgbLedSetPattern                   : [93]
  // Set one or more leds to the stored color by modulo
  , chainableRgbLedSetModulo                    : [94]
  // Sets leds similar to a bar graph, reversible
  , chainableRgbLedSetLevel                     : [95]

  // Grove IR sensor
  // Read the button from IR sensor
  , irRead                                      : [21]
  // Set pin for the IR reciever
  , irRecvPin                                   : [22]

  // Grove Dust sensor
  , dustSensorRead                              : [10]
  , dustSensorEn                                : [14]
  , dustSensorDis                               : [15]

  // Encoder
  , encoderRead                                 : [11]
  , encoderEn                                   : [16]
  , encoderDis                                  : [17]

  // Grove Flow sensor
  , flowRead                                    : [12]
  , flowEn                                      : [18]
  , flowDis                                     : [13]

  // This allows us to be more specific about which commands contain unused bytes
  , unused                                      : 0
};

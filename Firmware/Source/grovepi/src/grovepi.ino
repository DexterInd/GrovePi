#include "ChainableLED.h"
#include "DHT.h"
#include "Grove_LED_Bar.h"
#include "TM1637.h"
#include "TimerOne.h"
#include <IRremote.h>
#include <Wire.h>
#include <YetAnotherPcInt.h>

DHT dht;
Grove_LED_Bar ledbar[6]; // 7 instances for D2-D8, however, max 4 bars, you; can't use adjacent sockets, 4 pin display
TM1637 fourdigit[6];     // 7 instances for D2-D8, however, max 4 displays, you; can't use adjacent sockets, 4 pin display
ChainableLED rgbled[6];  // 7 instances for D2-D8

IRrecv irrecv;          // object to interface with the IR receiver
decode_results results; // results for the IR receiver

#define SLAVE_ADDRESS 0x04

// #define dust_sensor_read_cmd 10
// #define dust_sensor_en_cmd 14
// #define dust_sensor_dis_cmd 15
// #define dust_sensor_int_cmd 9
// #define dust_sensor_read_int_cmd 6

// #define encoder_read_cmd 11
// #define encoder_en_cmd 16
// #define encoder_dis_cmd 17

// #define flow_read_cmd 12
// #define flow_en_cmd 18
// #define flow_dis_cmd 13

#define ir_read_cmd 21
#define ir_recv_pin_cmd 22
#define ir_read_isdata 24

#define isr_set_cmd 6
#define isr_unset_cmd 9
#define isr_read_cmd 10
#define isr_clear_cmd 11
#define isr_active_cmd 12

#define encoder_read_cmd 13
#define encoder_en_cmd 14
#define encoder_dis_cmd 15

#define data_not_available 23

volatile uint8_t cmd[5];
volatile int index = 0;
volatile int flag = 0;
volatile byte b[21], float_array[4], dht_b[21];
volatile bool need_extra_loop = false;
int pin;

// for interrupt stuff
const uint8_t total_ports = 9;
enum ISR_Type {
  COUNT_CHANGES, COUNT_LOW_DURATION
};
typedef struct {
  volatile unsigned long period, last_update;
} Tracked_time;
typedef struct {
  volatile unsigned long counted_duration, pulse_end, pulse_start;
} Pulse_counter;

volatile uint8_t pins[total_ports]; // to track the available pins (passes the address to PcInt attachInterrupt method)
volatile bool set_pcint[total_ports]; // to see which ports are being watched
volatile uint8_t func_type[total_ports]; // type of counting function - COUNT_CHANGES or COUNT_LOW_DURATION
Tracked_time tracked_time[total_ports]; // for tracking the time
Pulse_counter pulse_counter[total_ports]; // for counting pulses
volatile unsigned long change_counter[total_ports]; // for counting changes
volatile uint32_t buffer[total_ports]; // to store the calculated values for transmission

// for encoders
typedef struct {
  volatile uint8_t LOW_PIN, HIGH_PIN;
  volatile int32_t value;
  volatile uint8_t MAX_VAL = 32;
} GroveEncoder;
GroveEncoder ge[total_ports];

volatile int run_once;
unsigned char dta[21];
int length, i;
int aRead = 0;
byte accFlag = 0, clkFlag = 0;
int8_t accv[3];
byte rgb[] = {0, 0, 0};

// all user-defined functions
void processIO();
void flushI2C();
void receiveData();
void sendData();
void detachISRPin(const uint8_t);
void isr_buffer_filler();
void isr_handler(uint8_t, bool);

void setup() {
  // Start serial
  Serial.begin(38400);

  // Start I2C
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);

  // Set port 4 to output and set it to LOW
  DDRD |= 0x10;
  PORTD &= ~0x10;

  // initialize the pins array with the ports itself
  for(int i = 0; i < total_ports; i++) {
    pins[i] = i;
  }

  Timer1.attachInterrupt(isr_buffer_filler, 1000);  // Buffer maintenance.
}

void processIO() {
  // Handles incoming data.
  // Updates sensors.
  // Sets output pins.

  if (index == 4 && flag == 0) {
    flag = 1;
    // Digital Read
    if (cmd[0] == 1)
    {
      b[0] = cmd[0];
      b[1] = digitalRead(cmd[1]);
    }

    // Digital Write
    else if (cmd[0] == 2)
      digitalWrite(cmd[1], cmd[2]);

    // Analog Read
    else if (cmd[0] == 3) {
      aRead = analogRead(cmd[1]);
      b[0] = cmd[0];
      b[1] = aRead / 256;
      b[2] = aRead % 256;
    }

    // Set up Analog Write
    else if (cmd[0] == 4)
      analogWrite(cmd[1], cmd[2]);

    // Set up pinMode
    else if (cmd[0] == 5)
      pinMode(cmd[1], cmd[2]);

    // Ultrasonic Read
    else if (cmd[0] == 7) {
      pin = cmd[1];
      pinMode(pin, OUTPUT);
      digitalWrite(pin, LOW);
      delayMicroseconds(2);
      digitalWrite(pin, HIGH);
      delayMicroseconds(5);
      digitalWrite(pin, LOW);
      pinMode(pin, INPUT);
      // setting timeout to 75000 microseconds
      // which is roughly the equivalent of time needed for the sound
      // to travel 10 meters from the sensor to the target
      // and backwards - where the speed of sound is 343m/s
      long dur = pulseIn(pin, HIGH, 75000);
      long RangeCm = dur / 29 / 2;
      b[0] = cmd[0];
      b[1] = RangeCm / 256;
      b[2] = RangeCm % 256;
      // Serial.println(b[1] * 256 + b[2]);
      // Serial.println(b[1]);
      // Serial.println(b[2]);
    }
    // Firmware version
    else if (cmd[0] == 8) {
      b[0] = cmd[0];
      b[1] = 1;
      b[2] = 4;
      b[3] = 0;
    }

    // Grove temp and humidity sensor pro
    // 40- Temperature
    else if (cmd[0] == 40) {
      if (run_once) {
        if (cmd[2] == 0)
          dht.begin(cmd[1], DHT11);
        else if (cmd[2] == 1)
          dht.begin(cmd[1], DHT22);
        else if (cmd[2] == 2)
          dht.begin(cmd[1], DHT21);
        else if (cmd[2] == 3)
          dht.begin(cmd[1], AM2301);
        float *buffer;
        buffer = dht.readTempHum();

        byte *b1 = (byte *)buffer;
        byte *b2 = (byte *)(buffer + 1);

        dht_b[0] = cmd[0];
        for (uint8_t j = 1; j < 5; j++)
          dht_b[j] = b1[j - 1];
        for (uint8_t j = 5; j < 9; j++)
          dht_b[j] = b2[j - 5];
        run_once = 0;
      }
    }

    // Grove LED Bar
    // http://www.seeedstudio.com/wiki/Grove_-_LED_Bar
    // pins: data,clock,vcc,gnd

    // Commands
    // [50, pin, greenToRed, unused]  initialise a LED Bar
    // [51, pin, greenToRed, unused]  setGreenToRed(bool greenToRed)
    // [52, pin, level, unused]       setLevel(unsigned char level)
    // [53, pin, led, state]          setLed(unsigned char led, bool state)
    // [54, pin, led, unused]         toggleLed(unsigned char led)
    // [55, pin, bits 1-8, bits 9-10] setBits(unsigned int bits)
    // [56, pin, unused, unused]      getBits()

    // Initialise
    // [50, pin, orientation, unused]
    else if (cmd[0] == 50) {
      // clock pin is always next to the data pin
      ledbar[cmd[1] - 2].begin(cmd[1] + 1, cmd[1],
                               cmd[2]); // clock, data, orientation
    }

    // Change the orientation
    // Green to red, or red to green
    // [51, pin, greenToRed, unused]
    else if (cmd[0] == 51 && ledbar[cmd[1] - 2].ready()) {
      ledbar[cmd[1] - 2].setGreenToRed(cmd[2]);
    }

    // Set level (0-10)
    // Level 0 means all leds off
    // Level 10 means all leds on
    // [52, pin, level, unused]
    else if (cmd[0] == 52 && ledbar[cmd[1] - 2].ready()) {
      ledbar[cmd[1] - 2].setLevel(cmd[2]);
    }

    // Set a single led
    // led (1-10)
    // state (0=off, 1=on)
    // [53, pin, led, state]
    else if (cmd[0] == 53 && ledbar[cmd[1] - 2].ready()) {
      ledbar[cmd[1] - 2].setLed(cmd[2], cmd[3]);
    }

    // Toggle a single led
    // led (1-10)
    // [54, pin, led, unused]
    else if (cmd[0] == 54 && ledbar[cmd[1] - 2].ready()) {
      ledbar[cmd[1] - 2].toggleLed(cmd[2]);
    }

    // Set the current state, one bit for each led
    // 0    = 0x0   = 0b000000000000000 = all leds off
    // 5    = 0x05  = 0b000000000000101 = leds 1 and 3 on, all others off
    // 341  = 0x155 = 0b000000101010101 = leds 1,3,5,7,9 on, 2,4,6,8,10 off
    // 1023 = 0x3ff = 0b000001111111111 = all leds on
    //                       |        |
    //                       10       1
    // [55, pin, bits 1-8, bits 9-10]
    else if (cmd[0] == 55 && ledbar[cmd[1] - 2].ready()) {
      ledbar[cmd[1] - 2].setBits(cmd[2] ^ (cmd[3] << 8));
    }

    // Return the current state
    // [56, pin, unused, unused]
    else if (cmd[0] == 56 && ledbar[cmd[1] - 2].ready()) {
      unsigned int state = ledbar[cmd[1] - 2].getBits();
      b[0] = cmd[0];
      b[1] = state & 0xFF;
      b[2] = state >> 8;
    }

    // end Grove LED Bar

    // Grove 4 Digit Display (7 segment)
    // http://www.seeedstudio.com/wiki/Grove_-_4-Digit_Display
    // pins: clock,data,vcc,gnd

    // Commands
    // [70, pin, unused, unused]      initialise a 4 digit display
    // [71, pin, brightness, unused]  set brightness
    // [72, pin, bits 1-8, bits 9-16] right aligned decimal value without
    // leading zeros [73, pin, bits 1-8, bits 9-16] right aligned decimal value
    // with leading zeros [74, pin, index, dec]          set individual digit
    // [75, pin, index, binary]       set individual segment
    // [76, pin, left, right]         set left and right values with colon
    // [77, pin, analog pin, seconds] display analog read for n seconds
    // [78, pin, unused, unused]      display on
    // [79, pin, unused, unused]      display off

    // initialise a 4 digit display
    // [70, pin, unused, unused]
    else if (cmd[0] == 70) {
      // clock pin is always next to the data pin
      fourdigit[cmd[1] - 2].begin(cmd[1], cmd[1] + 1); // clock, data
    }

    // set brightness
    // [71, pin, brightness, unused]
    else if (cmd[0] == 71 && fourdigit[cmd[1] - 2].ready()) {
      fourdigit[cmd[1] - 2].setBrightness(cmd[2]); // setBrightness(brightness)
    }

    // show right aligned decimal value without leading zeros
    // [72, pin, bits 1-8, bits 9-16]
    else if (cmd[0] == 72 && fourdigit[cmd[1] - 2].ready()) {
      fourdigit[cmd[1] - 2].showNumberDec(
          cmd[2] ^ (cmd[3] << 8), false); // showNumberDec(number, leading_zero)
    }

    // show right aligned decimal value with leading zeros
    // [73, pin, bits 1-8, bits 9-16]
    else if (cmd[0] == 73 && fourdigit[cmd[1] - 2].ready()) {
      fourdigit[cmd[1] - 2].showNumberDec(
          cmd[2] ^ (cmd[3] << 8), true); // showNumberDec(number, leading_zero)
    }

    // set individual digit
    // [74, pin, index, dec]
    else if (cmd[0] == 74 && fourdigit[cmd[1] - 2].ready()) {
      uint8_t data[] = {};
      data[0] =
          fourdigit[cmd[1] - 2].encodeDigit(cmd[3]); // encodeDigit(number)
      fourdigit[cmd[1] - 2].setSegments(
          data, 1, cmd[2]); // setSegments(segments[], length, position)
    }

    // set individual segment
    // [75, pin, index, binary]
    else if (cmd[0] == 75 && fourdigit[cmd[1] - 2].ready()) {
      // 0xFF = 0b11111111 = Colon,G,F,E,D,C,B,A
      // Colon only works on 2nd segment (index 1)
      //     -A-
      //  F |   | B
      //     -G-
      //  E |   | C
      //     -D-
      uint8_t data[] = {};
      data[0] = cmd[3]; // byte
      fourdigit[cmd[1] - 2].setSegments(
          data, 1, cmd[2]); // setSegments(segments[], length, position)
    }

    // set left and right with colon separator
    // [76, pin, left, right]
    else if (cmd[0] == 76 && fourdigit[cmd[1] - 2].ready()) {
      uint8_t data[] = {};
      // 1st segment
      data[0] =
          fourdigit[cmd[1] - 2].encodeDigit(cmd[2] / 10); // encodeDigit(number)
      // 2nd segment
      data[1] =
          fourdigit[cmd[1] - 2].encodeDigit(cmd[2] % 10); // encodeDigit(number)
      // colon
      data[1] |= 0x80;
      // 3rd segment
      data[2] =
          fourdigit[cmd[1] - 2].encodeDigit(cmd[3] / 10); // encodeDigit(number)
      // 4th segment
      data[3] =
          fourdigit[cmd[1] - 2].encodeDigit(cmd[3] % 10); // encodeDigit(number)
      // send
      fourdigit[cmd[1] - 2].setSegments(
          data, 4, 0); // setSegments(segments[], length, position)
    }

    // analog read
    // [77, pin, analog pin, seconds]
    else if (cmd[0] == 77 && fourdigit[cmd[1] - 2].ready()) {
      int pin = cmd[2];
      int reads = 4 * cmd[3]; // 1000/250 * cmd[3]

      // reading analog pin 4x per second
      for (int i = 0; i < reads; i++) {
        fourdigit[cmd[1] - 2].showNumberDec(
            analogRead(pin), false); // showNumberDec(number, leading_zero)
      }
    }

    // display on
    // [78, pin, unused, unused]
    else if (cmd[0] == 78 && fourdigit[cmd[1] - 2].ready()) {
      uint8_t data[] = {0xFF, 0xFF, 0xFF, 0xFF};
      fourdigit[cmd[1] - 2].setSegments(
          data, 4, 0); // setSegments(segments[], length, position)
    }

    // display off
    // [79, pin, unused, unused]
    else if (cmd[0] == 79 && fourdigit[cmd[1] - 2].ready()) {
      uint8_t data[] = {0x00, 0x00, 0x00, 0x00};
      fourdigit[cmd[1] - 2].setSegments(
          data, 4, 0); // setSegments(segments[], length, position)
    }

    // end Grove 4 Digit Display

    // Grove Chainable RGB LED
    // http://www.seeedstudio.com/wiki/Grove_-_Chainable_RGB_LED
    // pins: ci,di,vcc,gnd and co,do,vcc,gnd

    // Commands
    // [90, red, green, blue]                store color for later use
    // [91, pin, num leds, unused]           initialise a chain of leds
    // [92, pin, num leds, unused]           initialise a chain of leds and set
    // all to a test color [93, pin, pattern, which led]         set one or more
    // leds to the stored color by pattern [94, pin, led offset, modulo divisor]
    // set one or more leds to the stored color by modulo [95, pin, level,
    // reverse]             sets leds similar to a bar graph, reversible

    // Store RGB color for later use
    // [90, red, green, blue]
    else if (cmd[0] == 90) {
      rgb[0] = cmd[1];
      rgb[1] = cmd[2];
      rgb[2] = cmd[3];
    }

    // Initialise a RGB LED chain
    // [91, pin, num leds, unused]
    else if (cmd[0] == 91) {
      rgbled[cmd[1] - 2].begin(cmd[1], cmd[1] + 1,
                               cmd[2]); // clock, data, num leds
    }

    // Test colors, repeating red green blue
    // color code: 0 black (off), 1 blue, 2 green, 3 cyan, 4 red, 5 magenta, 6
    // yellow, 7 white [92, pin, num leds, color code]
    else if (cmd[0] == 92) {
      rgbled[cmd[1] - 2].begin(cmd[1], cmd[1] + 1, cmd[2]);

      // figure out which color to display, a single bit for each rgb led
      byte rr = ((cmd[3] & 4) >> 2) * 255, gg = ((cmd[3] & 2) >> 1) * 255,
           bb = ((cmd[3] & 1)) * 255;

      // set each led to the specified color
      for (int i = 0; i < cmd[2]; i++) {
        rgbled[cmd[1] - 2].setColorRGB(i, rr, gg, bb);
      }
    }

    // Set one or more leds to the stored color using pattern
    // pattern: 0 = this led only, 1 all leds except this led, 2 this led and
    // all leds inwards, 3 this led and all leds outwards which led: 0 = led
    // closest to the GrovePi, 1 = second led counting outwards [93, pin,
    // pattern, which led]
    else if (cmd[0] == 93) {
      if (cmd[2] == 0) {
        // set an individual led to the stored color
        rgbled[cmd[1] - 2].setColorRGB(cmd[3], rgb[0], rgb[1],
                                       rgb[2]); // which led, red, green, blue
      } else {
        // set all leds to stored color
        byte num_leds = rgbled[cmd[1] - 2].getNumLeds();

        for (int i = 0; i < num_leds; i++) {
          // cmd[2] == 1: set all leds other than this one to the stored color
          // cmd[2] == 2: this led and all previous leds, inwards
          // cmd[2] == 3: this led and all next leds, outwards
          if ((cmd[2] == 1 && i != cmd[3]) || (cmd[2] == 2 && i <= cmd[3]) ||
              (cmd[2] == 3 && i >= cmd[3])) {
            rgbled[cmd[1] - 2].setColorRGB(
                i, rgb[0], rgb[1], rgb[2]); // which led, red, green, blue
          }
        }
      }
    }

    // Set one or more leds to the stored color using modulo
    // led offset: 0 = led closest to the GrovePi, counting outwards
    // modulo divisor: when 1 (default) sets stored color on all leds >= offset,
    // when 2 sets every 2nd led >= offset and so on [94, pin, led offset,
    // modulo divisor]
    else if (cmd[0] == 94) {
      // modulo divisor must be >= 1
      if (cmd[3] < 1) {
        cmd[3] = 1;
      }

      // get the chain length
      byte num_leds = rgbled[cmd[1] - 2].getNumLeds();

      // starting at the offset, step through each led and if the result of the
      // modulo operator results in zero, set the stored color on the led
      for (int i = cmd[2]; i < num_leds; i++) {
        // use modulo to set every n led
        if ((i - cmd[2]) % cmd[3] == 0) {
          rgbled[cmd[1] - 2].setColorRGB(i, rgb[0], rgb[1],
                                         rgb[2]); // which led, red, green, blue
        }
      }
    }

    // Set level (0 to num leds), counting outwards from the GrovePi, 0 = all
    // off, 1 = first led, reversible to count inwards [95, pin, level, reverse]
    else if (cmd[0] == 95) {
      // get the chain length
      byte num_leds = rgbled[cmd[1] - 2].getNumLeds();

      if (cmd[3] == 0) {
        // outwards
        for (int i = 0; i < num_leds; i++) {
          if (cmd[2] > i) {
            rgbled[cmd[1] - 2].setColorRGB(
                i, rgb[0], rgb[1], rgb[2]); // which led, red, green, blue
          } else {
            rgbled[cmd[1] - 2].setColorRGB(i, 0, 0,
                                           0); // which led, red, green, blue
          }
        }
      } else {
        // inwards
        for (int i = num_leds; i > 0; i--) {
          if ((num_leds - cmd[2]) <= i) {
            rgbled[cmd[1] - 2].setColorRGB(
                i, rgb[0], rgb[1], rgb[2]); // which led, red, green, blue
          } else {
            rgbled[cmd[1] - 2].setColorRGB(i, 0, 0,
                                           0); // which led, red, green, blue
          }
        }
      }
    } else if (cmd[0] == ir_recv_pin_cmd) {
      Serial.print(cmd[1]);
      irrecv.setRecvpin(cmd[1]);
      irrecv.enableIRIn();
      cmd[0] = 0;
    } else if (cmd[0] == ir_read_cmd) {
      if (irrecv.decode(&results)) {
        b[0] = cmd[0];
        b[1] = results.decode_type;
        b[2] = results.address & 0xFF;
        b[3] = results.address >> 8;
        b[4] = results.value & 0xFF;
        b[5] = (results.value >> 8) & 0xFF;
        b[6] = (results.value >> 16) & 0xFF;
        b[7] = (results.value >> 24) & 0xFF;

        irrecv.resume(); // Receive the next value
      } else {
        b[0] = cmd[0];
        b[1] = results.decode_type;
      }
    } else if (cmd[0] == ir_read_isdata) {
      b[0] = cmd[0];
      b[1] = irrecv.decode(&results);
    }
  } else if (cmd[0] == isr_set_cmd) {

    if (run_once == 1) {
      uint8_t pin = cmd[1] & 0x0f; // 1st 4 bits to determine pin (D2->D8)
      const uint8_t ftype = (cmd[1] >> 4) & 0x03; // take 5th & 6th bits
      const uint8_t interrupt_mode = (cmd[1] >> 6) & 0x03; // take 7th and 8th bit
      const uint16_t period = (cmd[2] << 8) + cmd[3]; // get period in ms (maximum 65535 sms)

      // detach pin if it's already set
      if (set_pcint[pin]) {
        detachISRPin(pin);
      }

      pinMode(pin, INPUT_PULLUP);
      set_pcint[pin] = true;
      func_type[pin] = ftype;
      tracked_time[pin] = Tracked_time({period, 0});
      if (ftype == COUNT_CHANGES) {
        PcInt::attachInterrupt<uint8_t>(pin, isr_handler, (uint8_t*)&pins[pin], interrupt_mode, true);
      } else if (ftype == COUNT_LOW_DURATION) {
        pulse_counter[pin] = Pulse_counter({0, 0, 0});
        PcInt::attachInterrupt<uint8_t>(pin, isr_handler, (uint8_t*)&pins[pin], CHANGE, false);
      }
      run_once = 0;
    }

  } else if (cmd[0] == isr_unset_cmd) {

    if (run_once == 1) {
      // detach pin from PCINT
      const uint8_t pin = cmd[1];
      detachISRPin(pin);
      run_once = 0;
    }

  } else if (cmd[0] == isr_read_cmd) {

    if (run_once == 1) {
      const uint8_t pin = cmd[1]; // from pin D2->D8
      const uint32_t val = buffer[pin];
      b[0] = cmd[0];
      b[1] = val & 0xff;
      b[2] = (val >> 8) & 0xff;
      b[3] = (val >> 16) & 0xff;
      b[4] = (val >> 24) & 0xff;
      run_once = 0;
    }

  } else if (cmd[0] == isr_clear_cmd) {

    if (run_once == 1) {
      // detach all pins from PCINT
      for (int idx = 0; idx < total_ports; idx++) {
        if (set_pcint[idx]) {
          detachISRPin(idx);
        }
      }
    }

  } else if (cmd[0] == isr_active_cmd) {

    if (run_once == 1) {
      const uint8_t pin = cmd[1];

      if (pin > total_ports) {
        uint16_t ports = 0;
        for (int idx = 0; idx < total_ports; idx++) {
          ports += (set_pcint[idx] & 0x01) << idx;
        }

        b[0] = cmd[0];
        b[1] = ports & 0xff;
        b[2] = (ports >> 8) & 0xff;
      } else {
        b[0] = cmd[0];
        b[1] = 0;
        b[2] = (set_pcint[pin] & 0x01) << pin;
      }
      run_once = 0;
    }
  } else if (cmd[0] == encoder_en_cmd) {

    if (run_once == 1) {
      const uint8_t pin = cmd[1];
      const uint8_t steps = cmd[2];
      if (pin < total_ports - 1) {
          // detach pin if it's already set
        if (set_pcint[pin]) {
          detachISRPin(pin);
          detachISRPin(pin + 1);
        }
        ge[pin].LOW_PIN = pin;
        ge[pin].HIGH_PIN = pin + 1;
        ge[pin].value = 0;
        ge[pin].MAX_VAL = steps;
        pinMode(ge[pin].LOW_PIN, INPUT_PULLUP);
        pinMode(ge[pin].HIGH_PIN, INPUT_PULLUP);
        set_pcint[pin] = set_pcint[pin + 1] = true;
        PcInt::attachInterrupt<GroveEncoder>(ge[pin].LOW_PIN, grove_encoder_handler, &ge[pin], FALLING, false);
        PcInt::attachInterrupt<GroveEncoder>(ge[pin].HIGH_PIN, grove_encoder_handler, &ge[pin], FALLING, false);
      }
      run_once = 0;
    }

  } else if (cmd[0] == encoder_read_cmd) {

    if (run_once == 1) {
      const uint8_t pin = cmd[1];
      const int value = ge[pin].value;
      Serial.print(value);
      Serial.print("\n");

      b[0] = cmd[0];
      b[1] = value & 0xff;
      b[2] = (value >> 8) & 0xff;
      b[3] = (value >> 16) & 0xff;
      b[4] = (value >> 24) & 0xff;

      run_once = 0;
    }

  } else if (cmd[0] == encoder_dis_cmd) {

    if (run_once == 1) {
      const uint8_t pin = cmd[1];
      if (pin < total_ports - 1) {
        detachISRPin(pin);
        detachISRPin(pin + 1);
      }
      run_once = 0;
    }

  }
}

void loop() {
  if (need_extra_loop == true) {
    processIO();
    need_extra_loop = false;
  } else {
    processIO();
  }
}

void receiveData(int byteCount) {
  if (!need_extra_loop) {
    while (Wire.available()) {
      if (Wire.available() == 4) {
        flag = 0;
        index = 0;
        run_once = 1;
      }
      cmd[index++] = Wire.read();
    }
    need_extra_loop = true;
  } else {
    flushI2C();
  }
}

void flushI2C() {
  while (Wire.available())
    Wire.read();
}

// Callback for sending data
void sendData() {
    if (need_extra_loop == false) {
    if (cmd[0] == 1)
      Wire.write((byte *)b, 2);
    if (cmd[0] == 3 || cmd[0] == 7 || cmd[0] == 56)
      Wire.write((byte *)b, 3);
    if (cmd[0] == 8 || cmd[0] == 20)
      Wire.write((byte *)b, 4);
    if (cmd[0] == 30)
      Wire.write((byte *)b, 9);
    if (cmd[0] == 40)
      Wire.write((byte *)dht_b, 9);
    if (cmd[0] == isr_read_cmd)
      Wire.write((byte *)b, 5);
    if (cmd[0] == isr_active_cmd)
      Wire.write((byte *)b, 3);
    if (cmd[0] == ir_read_cmd) {
      Wire.write((byte *)b, 8);
      b[0] = 0;
    }
    if (cmd[0] == encoder_read_cmd) {
      Wire.write((byte *)b, 5);
    }
    if (cmd[0] == ir_read_isdata)
      Wire.write((byte *)b, 2);
  }
  // otherwise just reply the Pi telling
  // there's no data available yet
  else {
    Wire.write(data_not_available);
  }
}

// detaching an PCINT interrupt from a given pin
void detachISRPin(const uint8_t pin) {
  // detach pin from PCINT
  if (set_pcint[pin]) {
    PcInt::detachInterrupt(pin);
    pinMode(pin, OUTPUT);
    set_pcint[pin] = false;
  }
}

// repeatedly called ISR to update values on each interrupt-enabled pin
void isr_buffer_filler() {
  // PORTD |= 0x10;

  const unsigned long current = micros() / 1000;
  // iterate over all possible interrupted pins
  for (int idx = 0; idx < total_ports; idx++) {
    // if the pin has been attached to an interrupt
    if (set_pcint[idx]) {
      const unsigned long elapsed_time = current - tracked_time[idx].last_update;
      // if more time than the associated period has passed
      if (elapsed_time >= tracked_time[idx].period) {
          // save and reset depending on the selected function
          switch (func_type[idx]) {
            case COUNT_CHANGES:
              buffer[idx] = change_counter[idx];
              change_counter[idx] = 0;
              break;
            case COUNT_LOW_DURATION:
              buffer[idx] = pulse_counter[idx].counted_duration * tracked_time[idx].period / elapsed_time;
              pulse_counter[idx].counted_duration = 0;
              break;
          }
          // update time
          tracked_time[idx].last_update = current;
      }
    }
  }

  // PORTD &= ~0x10;
}

 // interrupt handler for COUNT_CHANGES & COUNT_LOW_DURATION operations
void isr_handler(uint8_t *userdata, bool newstate) {

  // PORTD |= 0x10;

  // const uint8_t pin = *((uint8_t*)userdata);
  const uint8_t pin = *userdata;

  if (func_type[pin] == COUNT_CHANGES) {

    // count changes
    change_counter[pin] ++;

  } else if (func_type[pin] == COUNT_LOW_DURATION) {

    // count duration
    if (newstate == 0) {
      pulse_counter[pin].pulse_start = micros();
    } else {
      pulse_counter[pin].pulse_end = micros();
    }
    const unsigned long pulse_end = pulse_counter[pin].pulse_end;
    const unsigned long pulse_start = pulse_counter[pin].pulse_start;
    if(pulse_end > pulse_start) {
      const unsigned long duration = int((pulse_end - pulse_start) / 1000); // to get ms
      pulse_counter[pin].counted_duration += duration;
      pulse_counter[pin].pulse_end = 0;
    }

  }

  // PORTD &= ~0x10;

}

// interrupt handler for grove encoders
void grove_encoder_handler(GroveEncoder *ge) {
  // PORTD |= 0x10;

  const uint8_t valA = digitalRead(ge->LOW_PIN);
  const uint8_t valB = digitalRead(ge->HIGH_PIN);

  if (valA + valB > 0 && valA + valB < 2) {
    if (valA < valB) {
      ge->value += 1;
    } else {
      ge->value -= 1;
    }
  }

  if (ge->value < 0)
    ge->value = 0;
  else if (ge->value > ge->MAX_VAL)
    ge->value = ge->MAX_VAL;

  Serial.println(ge->LOW_PIN);
  Serial.println(ge->HIGH_PIN);

  // PORTD &= ~0x10;
}

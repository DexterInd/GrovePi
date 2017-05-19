#include <Wire.h>
#include "DHT.h"
#include "Grove_LED_Bar.h"
#include "TM1637.h"
#include "ChainableLED.h"
#include "Encoder.h"
#include "TimerOne.h"

// Note that RCSwitch.h is a patched version of the one from the https://github.com/sui77/rc-switch repository.
// Additional functions have been added to get a numerical version of radio sequences sent/received.
#include "RCSwitch.h"

DHT dht;
Grove_LED_Bar ledbar[6];  // 7 instances for D2-D8, however, max 4 bars, you can't use adjacent sockets, 4 pin display
TM1637 fourdigit[6];      // 7 instances for D2-D8, however, max 4 displays, you can't use adjacent sockets, 4 pin display
ChainableLED rgbled[6];   // 7 instances for D2-D8

#define SLAVE_ADDRESS 0x04

#define dust_sensor_read_cmd    10
#define dust_sensor_en_cmd		14
#define dust_sensor_dis_cmd		15

#define encoder_read_cmd        11
#define encoder_en_cmd			16
#define encoder_dis_cmd			17

#define flow_read_cmd           12
#define flow_en_cmd				18
#define flow_dis_cmd       		13

#define rc_switch_send_cmd       110
#define rc_switch_subscribe_cmd  111
#define rc_switch_read_cmd		112
#define rc_switch_typeA          0
#define rc_switch_typeB          1
#define rc_switch_typeC          2
#define rc_switch_typeD          3
#define rc_switch_max_sub        8 // Max number of switch subscriptions

int cmd[5];
int index=0;
int flag=0;
int i;
byte val=0,b[21],float_array[4],dht_b[21];
unsigned char dta[21];
int length;
int aRead=0;
byte accFlag=0,clkFlag=0;
int8_t accv[3];
byte rgb[] = { 0, 0, 0 };
int run_once;

//Dust sensor variables:
unsigned long starttime;
unsigned long sampletime_ms = 30000;//sample 30s ;
unsigned long lowpulseoccupancy = 0, latest_dust_val=0;
unsigned long t, pulse_end,pulse_start,duration;
int dust_run_bk=0;
int dust_latest=0;
int l_status;

//Encoder variable
int index_LED;
byte enc_val[2];        //Given it's own I2C buffer so that it does not corrupt the data from other sensors when running in background 
int enc_run_bk=0;   //Flag for first time setup

//Flow sensor variables
volatile int NbTopsFan; //measuring the rising edges of the signal
int Calc;                               
int hallsensor = 2;    //The pin location of the sensor
int flow_run_bk=0;
long flow_read_start;
byte flow_val[3];        //Given it's own I2C buffer so that it does not corrupt the data from other sensors when running in background 

// 433MHz RCSwitch variables
RCSwitch rc_switch; // Library instance
// TODO define constants for on/off
uint8_t rc_switch_state; // Desired state of the remote-controlled switch. 0=OFF, 1=ON
uint8_t rc_switch_type; // Remote-controlled switch type. 0 == type A, 1 == type B, 2 == type C, 3 == type D.
char rc_switch_typeA_group [6]; // For type A switches, group DIP setting as a binary string ("00110" == OFF OFF ON ON OFF)
char rc_switch_typeA_device [6]; // For type A switches, device DIP setting as a binary string ("00110" == OFF OFF ON ON OFF)
struct rc_switch_subscription_struct { // Struct describing a subscription to a set of on/off codes
	unsigned long onCode = 0;
	unsigned long offCode = 0;
	byte lastStatus = 255; // 255: unknown
};
struct rc_switch_subscription_struct rc_switch_subscription[rc_switch_max_sub - 1]; // Subscription storage
uint8_t rc_switch_subscription_number;
boolean rc_switch_run_bk = false;
unsigned long rc_switch_code;

void setup()
{
    // Serial.begin(38400);         // start serial for output
    Wire.begin(SLAVE_ADDRESS);

    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);
}
int pin;
int j;
void loop()
{
	long dur,RangeCm;
	if(index==4 && flag == 0 )
	{
		flag=1;
		//Digital Read
		if(cmd[0]==1)
		  val=digitalRead(cmd[1]);

		//Digital Write
		else if(cmd[0]==2)
		  digitalWrite(cmd[1],cmd[2]);

		//Analog Read
		else if(cmd[0]==3)
		{
		  aRead=analogRead(cmd[1]);
		  b[1]=aRead/256;
		  b[2]=aRead%256;
		}

		//Set up Analog Write
		else if(cmd[0]==4)
		  analogWrite(cmd[1],cmd[2]);

		//Set up pinMode
		else if(cmd[0]==5)
		  pinMode(cmd[1],cmd[2]);

		//Ultrasonic Read
		else if(cmd[0]==7)
		{
		  pin=cmd[1];
		  pinMode(pin, OUTPUT);
		  digitalWrite(pin, LOW);
		  delayMicroseconds(2);
		  digitalWrite(pin, HIGH);
		  delayMicroseconds(5);
		  digitalWrite(pin,LOW);
		  pinMode(pin,INPUT);
		  dur = pulseIn(pin,HIGH);
		  RangeCm = dur/29/2;
		  b[1]=RangeCm/256;
		  b[2]=RangeCm%256;
		  //Serial.println(b[1]);
		  //Serial.println(b[2]);
		}
		//Firmware version
		else if(cmd[0]==8)
		{
		  b[1] = 1;
		  b[2] = 2;
		  b[3] = 7;
		}
	 
		//Grove temp and humidity sensor pro
		//40- Temperature
		else if(cmd[0]==40)
		{
			if(run_once)
			{
				if(cmd[2]==0)
					dht.begin(cmd[1],DHT11);
				else if(cmd[2]==1)
					dht.begin(cmd[1],DHT22);
				else if(cmd[2]==2)
					dht.begin(cmd[1],DHT21);
				else if(cmd[2]==3)
					dht.begin(cmd[1],AM2301);
				float t= dht.readTemperature();
				float h= dht.readHumidity();
				//Serial.print(t);
				//Serial.print("#");
				byte *b1=(byte*)&t;
				byte *b2=(byte*)&h;
				for(j=0;j<4;j++)
				dht_b[j+1]=b1[j];
				for(j=4;j<8;j++)
				dht_b[j+1]=b2[j-4];
				run_once=0;
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
		else if(cmd[0] == 50)
		{
		  // clock pin is always next to the data pin
		  ledbar[cmd[1]-2].begin(cmd[1]+1, cmd[1], cmd[2]); // clock, data, orientation
		}

		// Change the orientation
		// Green to red, or red to green
		// [51, pin, greenToRed, unused]
		else if(cmd[0] == 51 && ledbar[cmd[1]-2].ready())
		{
		  ledbar[cmd[1]-2].setGreenToRed(cmd[2]);
		}

		// Set level (0-10)
		// Level 0 means all leds off
		// Level 10 means all leds on
		// [52, pin, level, unused]
		else if(cmd[0] == 52 && ledbar[cmd[1]-2].ready())
		{
		  ledbar[cmd[1]-2].setLevel(cmd[2]);
		}

		// Set a single led
		// led (1-10)
		// state (0=off, 1=on)
		// [53, pin, led, state]
		else if(cmd[0] == 53 && ledbar[cmd[1]-2].ready())
		{
		  ledbar[cmd[1]-2].setLed(cmd[2], cmd[3]);
		}

		// Toggle a single led
		// led (1-10)
		// [54, pin, led, unused]
		else if(cmd[0] == 54 && ledbar[cmd[1]-2].ready())
		{
		  ledbar[cmd[1]-2].toggleLed(cmd[2]);
		}

		// Set the current state, one bit for each led
		// 0    = 0x0   = 0b000000000000000 = all leds off
		// 5    = 0x05  = 0b000000000000101 = leds 1 and 3 on, all others off
		// 341  = 0x155 = 0b000000101010101 = leds 1,3,5,7,9 on, 2,4,6,8,10 off
		// 1023 = 0x3ff = 0b000001111111111 = all leds on
		//                       |        |
		//                       10       1
		// [55, pin, bits 1-8, bits 9-10]
		else if(cmd[0] == 55 && ledbar[cmd[1]-2].ready())
		{
		  ledbar[cmd[1]-2].setBits(cmd[2] ^ (cmd[3] << 8));
		}

		// Return the current state
		// [56, pin, unused, unused]
		else if(cmd[0] == 56 && ledbar[cmd[1]-2].ready())
		{
		  unsigned int state = ledbar[cmd[1]-2].getBits();
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
		// [72, pin, bits 1-8, bits 9-16] right aligned decimal value without leading zeros
		// [73, pin, bits 1-8, bits 9-16] right aligned decimal value with leading zeros
		// [74, pin, index, dec]          set individual digit
		// [75, pin, index, binary]       set individual segment
		// [76, pin, left, right]         set left and right values with colon
		// [77, pin, analog pin, seconds] display analog read for n seconds
		// [78, pin, unused, unused]      display on
		// [79, pin, unused, unused]      display off

		// initialise a 4 digit display
		// [70, pin, unused, unused]
		else if(cmd[0] == 70)
		{
		  // clock pin is always next to the data pin
		  fourdigit[cmd[1]-2].begin(cmd[1], cmd[1]+1);  // clock, data
		}

		// set brightness
		// [71, pin, brightness, unused]
		else if(cmd[0] == 71 && fourdigit[cmd[1]-2].ready())
		{
		  fourdigit[cmd[1]-2].setBrightness(cmd[2]);  // setBrightness(brightness)
		}

		// show right aligned decimal value without leading zeros
		// [72, pin, bits 1-8, bits 9-16]
		else if(cmd[0] == 72 && fourdigit[cmd[1]-2].ready())
		{
		  fourdigit[cmd[1]-2].showNumberDec(cmd[2] ^ (cmd[3] << 8), false);  // showNumberDec(number, leading_zero)
		}

		// show right aligned decimal value with leading zeros
		// [73, pin, bits 1-8, bits 9-16]
		else if(cmd[0] == 73 && fourdigit[cmd[1]-2].ready())
		{
		  fourdigit[cmd[1]-2].showNumberDec(cmd[2] ^ (cmd[3] << 8), true);  // showNumberDec(number, leading_zero)
		}

		// set individual digit
		// [74, pin, index, dec]
		else if(cmd[0] == 74 && fourdigit[cmd[1]-2].ready())
		{
		  uint8_t data[] = {};
		  data[0] = fourdigit[cmd[1]-2].encodeDigit(cmd[3]);  // encodeDigit(number)
		  fourdigit[cmd[1]-2].setSegments(data, 1, cmd[2]);  // setSegments(segments[], length, position)
		}

		// set individual segment
		// [75, pin, index, binary]
		else if(cmd[0] == 75 && fourdigit[cmd[1]-2].ready())
		{
		  // 0xFF = 0b11111111 = Colon,G,F,E,D,C,B,A
		  // Colon only works on 2nd segment (index 1)
		  //     -A-
		  //  F |   | B
		  //     -G-
		  //  E |   | C
		  //     -D-
		  uint8_t data[] = {};
		  data[0] = cmd[3];  // byte
		  fourdigit[cmd[1]-2].setSegments(data, 1, cmd[2]);  // setSegments(segments[], length, position)
		}

		// set left and right with colon separator
		// [76, pin, left, right]
		else if(cmd[0] == 76 && fourdigit[cmd[1]-2].ready())
		{
		  uint8_t data[] = {};
		  // 1st segment
		  data[0] = fourdigit[cmd[1]-2].encodeDigit(cmd[2] / 10);  // encodeDigit(number)
		  // 2nd segment
		  data[1] = fourdigit[cmd[1]-2].encodeDigit(cmd[2] % 10);  // encodeDigit(number)
		  // colon
		  data[1] |= 0x80;
		  // 3rd segment
		  data[2] = fourdigit[cmd[1]-2].encodeDigit(cmd[3] / 10);  // encodeDigit(number)
		  // 4th segment
		  data[3] = fourdigit[cmd[1]-2].encodeDigit(cmd[3] % 10);  // encodeDigit(number)
		  // send
		  fourdigit[cmd[1]-2].setSegments(data, 4, 0);  // setSegments(segments[], length, position)
		}

		// analog read
		// [77, pin, analog pin, seconds]
		else if(cmd[0] == 77 && fourdigit[cmd[1]-2].ready())
		{
		  int pin = cmd[2];
		  int reads = 4 * cmd[3];  // 1000/250 * cmd[3]

		  // reading analog pin 4x per second
		  for(int i = 0; i < reads; i++) {
			fourdigit[cmd[1]-2].showNumberDec(analogRead(pin), false);  // showNumberDec(number, leading_zero)
			delay(250);
		  }
		}

		// display on
		// [78, pin, unused, unused]
		else if(cmd[0] == 78 && fourdigit[cmd[1]-2].ready())
		{
		  uint8_t data[] = { 0xFF, 0xFF, 0xFF, 0xFF };
		  fourdigit[cmd[1]-2].setSegments(data, 4, 0);  // setSegments(segments[], length, position)
		}

		// display off
		// [79, pin, unused, unused]
		else if(cmd[0] == 79 && fourdigit[cmd[1]-2].ready())
		{
		  uint8_t data[] = { 0x00, 0x00, 0x00, 0x00 };
		  fourdigit[cmd[1]-2].setSegments(data, 4, 0);  // setSegments(segments[], length, position)
		}

		// end Grove 4 Digit Display
		
		// Grove Chainable RGB LED
		// http://www.seeedstudio.com/wiki/Grove_-_Chainable_RGB_LED
		// pins: ci,di,vcc,gnd and co,do,vcc,gnd
		
		// Commands
		// [90, red, green, blue]                store color for later use
		// [91, pin, num leds, unused]           initialise a chain of leds
		// [92, pin, num leds, unused]           initialise a chain of leds and set all to a test color
		// [93, pin, pattern, which led]         set one or more leds to the stored color by pattern
		// [94, pin, led offset, modulo divisor] set one or more leds to the stored color by modulo
		// [95, pin, level, reverse]             sets leds similar to a bar graph, reversible

		// Store RGB color for later use
		// [90, red, green, blue]
		else if(cmd[0] == 90)
		{
		  rgb[0] = cmd[1];
		  rgb[1] = cmd[2];
		  rgb[2] = cmd[3];
		}

		// Initialise a RGB LED chain
		// [91, pin, num leds, unused]
		else if(cmd[0] == 91)
		{
		  rgbled[cmd[1]-2].begin(cmd[1], cmd[1]+1, cmd[2]);  // clock, data, num leds
		}
		
		// Test colors, repeating red green blue
		// color code: 0 black (off), 1 blue, 2 green, 3 cyan, 4 red, 5 magenta, 6 yellow, 7 white
		// [92, pin, num leds, color code]
		else if(cmd[0] == 92)
		{
		  rgbled[cmd[1]-2].begin(cmd[1], cmd[1]+1, cmd[2]);
		  
		  // figure out which color to display, a single bit for each rgb led
		  byte rr = ((cmd[3] & 4) >> 2) * 255,
			   gg = ((cmd[3] & 2) >> 1) * 255,
			   bb = ((cmd[3] & 1)) * 255;

		  // set each led to the specified color
		  for(int i = 0; i < cmd[2]; i++)
		  {
			rgbled[cmd[1]-2].setColorRGB(i, rr, gg, bb);
		  }
		}

		// Set one or more leds to the stored color using pattern
		// pattern: 0 = this led only, 1 all leds except this led, 2 this led and all leds inwards, 3 this led and all leds outwards
		// which led: 0 = led closest to the GrovePi, 1 = second led counting outwards
		// [93, pin, pattern, which led]
		else if(cmd[0] == 93)
		{
		  if(cmd[2] == 0) {
			// set an individual led to the stored color
			rgbled[cmd[1]-2].setColorRGB(cmd[3], rgb[0], rgb[1], rgb[2]);  // which led, red, green, blue
		  }
		  else {
			// set all leds to stored color
			byte num_leds = rgbled[cmd[1]-2].getNumLeds();

			for(int i = 0; i < num_leds; i++)
			{
			  // cmd[2] == 1: set all leds other than this one to the stored color
			  // cmd[2] == 2: this led and all previous leds, inwards
			  // cmd[2] == 3: this led and all next leds, outwards
			  if((cmd[2] == 1 && i != cmd[3]) || (cmd[2] == 2 && i <= cmd[3]) || (cmd[2] == 3 && i >= cmd[3])) {
				rgbled[cmd[1]-2].setColorRGB(i, rgb[0], rgb[1], rgb[2]);  // which led, red, green, blue
			  }
			}
		  }
		}
		
		// Set one or more leds to the stored color using modulo
		// led offset: 0 = led closest to the GrovePi, counting outwards
		// modulo divisor: when 1 (default) sets stored color on all leds >= offset, when 2 sets every 2nd led >= offset and so on
		// [94, pin, led offset, modulo divisor]
		else if(cmd[0] == 94)
		{
		  // modulo divisor must be >= 1
		  if(cmd[3] < 1) {
			cmd[3] = 1;
		  }

		  // get the chain length
		  byte num_leds = rgbled[cmd[1]-2].getNumLeds();
		  
		  // starting at the offset, step through each led and if the result of the modulo operator results in zero, set the stored color on the led
		  for(int i = cmd[2]; i < num_leds; i++)
		  {
			// use modulo to set every n led
			if((i - cmd[2]) % cmd[3] == 0) {
			  rgbled[cmd[1]-2].setColorRGB(i, rgb[0], rgb[1], rgb[2]);  // which led, red, green, blue
			}
		  }
		}
		
		// Set level (0 to num leds), counting outwards from the GrovePi, 0 = all off, 1 = first led, reversible to count inwards
		// [95, pin, level, reverse]
		else if(cmd[0] == 95)
		{
		  // get the chain length
		  byte num_leds = rgbled[cmd[1]-2].getNumLeds();

		  if(cmd[3] == 0)
		  {
			// outwards
			for(int i = 0; i < num_leds; i++)
			{
			  if(cmd[2] > i) {
				rgbled[cmd[1]-2].setColorRGB(i, rgb[0], rgb[1], rgb[2]);  // which led, red, green, blue
			  }
			  else {
				rgbled[cmd[1]-2].setColorRGB(i, 0, 0, 0);  // which led, red, green, blue
			  }
			}
		  }
		  else {
			// inwards
			for(int i = num_leds; i > 0; i--)
			{
			  if((num_leds - cmd[2]) <= i) {
				rgbled[cmd[1]-2].setColorRGB(i, rgb[0], rgb[1], rgb[2]);  // which led, red, green, blue
			  }
			  else {
				rgbled[cmd[1]-2].setColorRGB(i, 0, 0, 0);  // which led, red, green, blue
			  }
			}
		  }
		}
		else if(cmd[0]==dust_sensor_en_cmd)
		{
			attachInterrupt(0,readPulseDust,CHANGE);
			dust_run_bk=1;
			starttime=millis();
			cmd[0]=0;
		}
		else if(cmd[0]==dust_sensor_dis_cmd)
		{
			detachInterrupt(0);
			dust_run_bk=0;
			cmd[0]=0;
		}
		else if(cmd[0]==dust_sensor_read_cmd)
		{
			if(run_once==1)
			{
			b[0]=dust_latest;
			b[1]=latest_dust_val%256;
			latest_dust_val=latest_dust_val/256;
			b[2]=latest_dust_val%256;
			b[3]=latest_dust_val/256;
			run_once=0;
			}
		}
		else if(cmd[0]==encoder_en_cmd)
		{
			encoder.Timer_init(); 
			enc_run_bk=1;
			cmd[0]=0;
		}
		else if(cmd[0]==encoder_dis_cmd)
		{
			encoder.Timer_disable();
			enc_run_bk=0;
		}
		else if(cmd[0]==flow_en_cmd)
		{
			pinMode(2, INPUT); 
			attachInterrupt(0, rpm, RISING);
			NbTopsFan = 0;
			flow_read_start=millis();
			flow_run_bk=1;
			cmd[0]=0;
		}
		else if(cmd[0]==flow_dis_cmd)
		{
			flow_run_bk=0;
			detachInterrupt(0);
			cmd[0]=0;
		}
		/* Command 110 - 433MHz transmitter: send command to radio-controlled switch or socket.
         *
         * Based on the RCSwitch library (https://github.com/sui77/rc-switch)
         * This library supports 4 types of switches, with different parameters.
         * For each of these, the firmware expects different parameters, as follows:
         *
         * +-------------------------------------------------------------------------------+
         * | Type A switch                                                                 |
         * +---------+---------+-----------------------------------------------------------+
         * | Byte    | Bits    | Description                                               |
         * +---------+---------+-----------------------------------------------------------+
         * |      1  | 0 - 7   | Command byte: send command to RC switch.                  |
         * |         |         | Decimal value: 110                                        |
         * +---------+---------+-----------------------------------------------------------+
         * |      2  | 0       | Pin on which the 433 MHz transmitter module is connected. |
         * |         |         | 0 -> D2 / 1 -> D3                                         |
         * |         +---------+-----------------------------------------------------------+
         * |         | 1 - 4   | Unused                                                    |
         * |         |         |                                                           |
         * |         +---------+-----------------------------------------------------------+
         * |         | 5       | Requested switch state.                                   |
         * |         |         | 0 = off / 1 = on                                          |
         * |         +---------+-----------------------------------------------------------+
         * |         | 6 - 7   | RC switch type.                                           |
         * |         |         | Type A: 00                                                |
         * +---------+---------+-----------------------------------------------------------+
         * |       3 | 0 - 4   | Group DIP switch.                                         |
         * |         |         | Ex: OFF-ON-ON-ON-OFF --> 01110                            |
         * |         +---------+-----------------------------------------------------------+
         * |         | 5 - 7   | Unused                                                    |
         * |         |         |                                                           |
         * +---------+---------+-----------------------------------------------------------+
         * |       4 | 0 - 4   | Device DIP switch.                                        |
         * |         |         | Ex: OFF-ON-ON-ON-OFF --> 01110                            |
         * |         +---------+-----------------------------------------------------------+
         * |         | 5 - 7   | Unused                                                    |
         * |         |         |                                                           |
         * +---------+---------+-----------------------------------------------------------+
         *
         *
         * +-------------------------------------------------------------------------------+
         * | Type B switch                                                                 |
         * +---------+---------+-----------------------------------------------------------+
         * | Byte    | Bits    | Description                                               |
         * +---------+---------+-----------------------------------------------------------+
         * |      1  | 0 - 7   | Command byte: send command to RC switch.                  |
         * |         |         | Decimal value: 110                                        |
         * +---------+---------+-----------------------------------------------------------+
         * |      2  | 0       | Pin on which the 433 MHz transmitter module is connected. |
         * |         |         | 0 -> D2 / 1 -> D3                                         |
         * |         +---------+-----------------------------------------------------------+
         * |         | 1 - 4   | Unused                                                    |
         * |         |         |                                                           |
         * |         +---------+-----------------------------------------------------------+
         * |         | 5       | Requested switch state.                                   |
         * |         |         | 0 = off / 1 = on                                          |
         * |         +---------+-----------------------------------------------------------+
         * |         | 6 - 7   | RC switch type.                                           |
         * |         |         | Type B: 01                                                |
         * +---------+---------+-----------------------------------------------------------+
         * |       3 | 0 - 7   | Group id (1 - 4).                                         |
         * |         |         | Ex: 3 --> 0000 0011                                       |
         * +---------+---------+-----------------------------------------------------------+
         * |       4 | 0 - 7   | Device id (1 - 4).                                        |
         * |         |         | Ex: 3 --> 0000 0011                                       |
         * +---------+---------+-----------------------------------------------------------+
         *
         *
         * +-------------------------------------------------------------------------------+
         * | Type C switch                                                                 |
         * +---------+---------+-----------------------------------------------------------+
         * | Byte    | Bits    | Description                                               |
         * +---------+---------+-----------------------------------------------------------+
         * |      1  | 0 - 7   | Command byte: send command to RC switch.                  |
         * |         |         | Decimal value: 110                                        |
         * +---------+---------+-----------------------------------------------------------+
         * |      2  | 0       | Pin on which the 433 MHz transmitter module is connected. |
         * |         |         | 0 -> D2 / 1 -> D3                                         |
         * |         +---------+-----------------------------------------------------------+
         * |         | 1 - 4   | Unused                                                    |
         * |         |         |                                                           |
         * |         +---------+-----------------------------------------------------------+
         * |         | 5       | Requested switch state.                                   |
         * |         |         | 0 = off / 1 = on                                          |
         * |         +---------+-----------------------------------------------------------+
         * |         | 6 - 7   | RC switch type.                                           |
         * |         |         | Type C: 10                                                |
         * +---------+---------+-----------------------------------------------------------+
         * |       3 | 0 - 7   | Device family ('a' - 'f'), as the ASCII code of the       |
         * |         |         | desired letter.                                           |
         * |         |         | Ex: 'b' --> 0110 0001                                     |
         * +---------+---------+-----------------------------------------------------------+
         * |       4 | 0 - 1   | Device id (1 - 4), minus 1.                               |
         * |         |         | Ex: device #3 --> 10                                      |
         * |         +---------+-----------------------------------------------------------+
         * |         | 2 - 3   | Device group (1 - 4), minus 1.                            |
         * |         |         | Ex: group #1 --> 00                                       |
         * |         +---------+-----------------------------------------------------------+
         * |         | 4 - 7   | Unused                                                    |
         * |         |         |                                                           |
         * +---------+---------+-----------------------------------------------------------+
         *
         *
         * +-------------------------------------------------------------------------------+
         * | Type D switch                                                                 |
         * +---------+---------+-----------------------------------------------------------+
         * | Byte    | Bits    | Description                                               |
         * +---------+---------+-----------------------------------------------------------+
         * |      1  | 0 - 7   | Command byte: send command to RC switch.                  |
         * |         |         | Decimal value: 110                                        |
         * +---------+---------+-----------------------------------------------------------+
         * |      2  | 0       | Pin on which the 433 MHz transmitter module is connected. |
         * |         |         | 0 -> D2 / 1 -> D3                                         |
         * |         +---------+-----------------------------------------------------------+
         * |         | 1 - 4   | Unused                                                    |
         * |         |         |                                                           |
         * |         +---------+-----------------------------------------------------------+
         * |         | 5       | Requested switch state.                                   |
         * |         |         | 0 = off / 1 = on                                          |
         * |         +---------+-----------------------------------------------------------+
         * |         | 6 - 7   | RC switch type.                                           |
         * |         |         | Type D: 11                                                |
         * +---------+---------+-----------------------------------------------------------+
         * |       3 | 0 - 7   | Device family ('A' - 'D'), as the ASCII code of the       |
         * |         |         | desired letter.                                           |
         * |         |         | Ex: 'C' --> 0100 0011                                     |
         * +---------+---------+-----------------------------------------------------------+
         * |       4 | 0 - 7   | Device id (1 - 3).                                        |
         * |         |         | Ex: 3 --> 0000 0011                                       |
         * +---------+---------+-----------------------------------------------------------+
         */
		else if (cmd[0]==rc_switch_send_cmd) {
			if (run_once == 1) {// Ensure we do not repeatedly execute this command while waiting for another one

				// Apply bit-mask to recover data from the 2nd command byte
                // pin: bit 0 of 2nd byte. 0 --> pin 2. 1 --> pin 3.
				pin = 2 + (cmd[1] & 1);
				// state (on/off) : bit 5
				rc_switch_state = uint8_t(cmd[1] >> 5 & 1);
				// remote switch type: 4 possible types encoded in bits 6-7
				rc_switch_type = uint8_t(cmd[1] >> 6);

				// Enable radio
				rc_switch.enableTransmit(pin);

				// Handle remaining bytes depending on the switch type
				switch (rc_switch_type) {
					case rc_switch_typeA: {
						// For this type of remote controlled switches, the RCSwitch library requires 2 parameters, group and
						// device, as 5-chars binary strings, padded with zeroes. These parameters should match DIP switches present
						// on the switch device.
						// Ex: a DIP switch set as OFF-ON-ON-ON-OFF is represented by the parameter string "01110"

						// Conversion of the group parameter in the appropriate format
						for (i = 4; i >= 0; --i) {
							rc_switch_typeA_group[4 - i] = (cmd[2] & (1 << i) ? '1' : '0');
						}
						rc_switch_typeA_group[5] = '\0';

						// Conversion of the device parameter in the appropriate format
						for (i = 4; i >= 0; --i) {
							rc_switch_typeA_device[4 - i] = (cmd[3] & (1 << i) ? '1' : '0');
						}
						rc_switch_typeA_device[5] = '\0';


						if (rc_switch_state == 0) {
							rc_switch.switchOff(rc_switch_typeA_group, rc_switch_typeA_device);
							rc_switch_code = rc_switch.switchOffCode(rc_switch_typeA_group, rc_switch_typeA_device);
						} else {
							rc_switch.switchOn(rc_switch_typeA_group, rc_switch_typeA_device);
							rc_switch_code = rc_switch.switchOnCode(rc_switch_typeA_group, rc_switch_typeA_device);
						}
						break;
					}
					case rc_switch_typeB: {
						// For this type of remote controlled switches, the RCSwitch library requires two parameters:
						// group as an int [1..4] --> directly passed in 3rd byte cmd[2]
						// device as an int [1..4] --> directly passed in 4th byte cmd[3]
						if (rc_switch_state == 0) {
							rc_switch.switchOff(cmd[2], cmd[3]);
							rc_switch_code = rc_switch.switchOffCode(cmd[2], cmd[3]);
						} else {
							rc_switch.switchOn(cmd[2], cmd[3]);
							rc_switch_code = rc_switch.switchOnCode(cmd[2], cmd[3]);
						}
						break;
					}
					case rc_switch_typeC: {
						// For this type of remote controlled switches, the RCSwitch library requires three parameters:
						// family code as a char ['a'..'f'] --> directly passed in 3rd byte cmd[2]
						// group as int [1..4] --> this value minus one is passed using bits 2 and 3 of the 4th byte cmd[3]
						// device as int [1..4] --> this value minus one is passed using bits 0 and 1 of the 4th byte cmd[3]
						if (rc_switch_state == 0) {
							rc_switch.switchOff(char(cmd[2]), 1 + (cmd[3] >> 2 & 3), 1 + (cmd[3] & 3));
							rc_switch_code = rc_switch.switchOffCode(char(cmd[2]), 1 + (cmd[3] >> 2 & 3), 1 + (cmd[3] & 3));
						} else {
							rc_switch.switchOn(char(cmd[2]), 1 + (cmd[3] >> 2 & 3), 1 + (cmd[3] & 3));
							rc_switch_code = rc_switch.switchOnCode(char(cmd[2]), 1 + (cmd[3] >> 2 & 3), 1 + (cmd[3] & 3));
						}
						break;
					}
					case rc_switch_typeD: {
						// For this type of remote controlled switches, the RCSwitch library requires two parameters:
						// group as a char ['A'..'D'] --> directly passed in 3rd byte cmd[2]
						// device as an int [1..3] --> directly passed in 4th byte cmd[3]
						if (rc_switch_state == 0) {
							rc_switch.switchOff(char(cmd[2]), cmd[3]);
							rc_switch_code = rc_switch.switchOffCode(char(cmd[2]), cmd[3]);
						} else {
							rc_switch.switchOn(char(cmd[2]), cmd[3]);
							rc_switch_code = rc_switch.switchOffCode(char(cmd[2]), cmd[3]);
						}
						break;
					}
					default: {
						// Unknown switch type --> do nothing
					}
				}
				// Disable radio
				rc_switch.disableTransmit();
			}
			cmd[0] = 0;
			run_once = 0;
		}
        /* Command 111 - 433MHz receiver: subscribe to radio commands
         *
         * Based on the RCSwitch library (https://github.com/sui77/rc-switch)
         * This library supports 4 types of switches, with different parameters.
         * For each of these, the firmware expects different parameters, as follows:
         *
         * +-------------------------------------------------------------------------------+
         * | Type A switch                                                                 |
         * +---------+---------+-----------------------------------------------------------+
         * | Byte    | Bits    | Description                                               |
         * +---------+---------+-----------------------------------------------------------+
         * |      1  | 0 - 7   | Command byte: subscribe to RC switch commands.            |
         * |         |         | Decimal value: 111                                        |
         * +---------+---------+-----------------------------------------------------------+
         * |      2  | 0       | Pin on which the 433 MHz receiver module is connected.    |
         * |         |         | 0 -> D2 / 1 -> D3                                         |
         * |         +---------+-----------------------------------------------------------+
         * |         | 1 - 3   | Subscription number                                       |
         * |         |         |                                                           |
         * |         +---------+-----------------------------------------------------------+
         * |         | 4       | Unused                                                    |
         * |         |         |                                                           |
         * |         +---------+-----------------------------------------------------------+
         * |         | 5       | Initial state.                                            |
         * |         |         | 0 = off / 1 = on                                          |
         * |         +---------+-----------------------------------------------------------+
         * |         | 6 - 7   | RC switch type.                                           |
         * |         |         | Type A: 00                                                |
         * +---------+---------+-----------------------------------------------------------+
         * |       3 | 0 - 4   | Group DIP switch.                                         |
         * |         |         | Ex: OFF-ON-ON-ON-OFF --> 01110                            |
         * |         +---------+-----------------------------------------------------------+
         * |         | 5 - 7   | Unused                                                    |
         * |         |         |                                                           |
         * +---------+---------+-----------------------------------------------------------+
         * |       4 | 0 - 4   | Device DIP switch.                                        |
         * |         |         | Ex: OFF-ON-ON-ON-OFF --> 01110                            |
         * |         +---------+-----------------------------------------------------------+
         * |         | 5 - 7   | Unused                                                    |
         * |         |         |                                                           |
         * +---------+---------+-----------------------------------------------------------+
         *
         *
         * +-------------------------------------------------------------------------------+
         * | Type B switch                                                                 |
         * +---------+---------+-----------------------------------------------------------+
         * | Byte    | Bits    | Description                                               |
         * +---------+---------+-----------------------------------------------------------+
         * |      1  | 0 - 7   | Command byte: subscribe to RC switch commands.            |
         * |         |         | Decimal value: 111                                        |
         * +---------+---------+-----------------------------------------------------------+
         * |      2  | 0       | Pin on which the 433 MHz receiver module is connected.    |
         * |         |         | 0 -> D2 / 1 -> D3                                         |
         * |         +---------+-----------------------------------------------------------+
         * |         | 1 - 3   | Subscription number                                       |
         * |         |         |                                                           |
         * |         +---------+-----------------------------------------------------------+
         * |         | 4       | Unused                                                    |
         * |         |         |                                                           |
         * |         +---------+-----------------------------------------------------------+
         * |         | 5       | Initial state.                                            |
         * |         |         | 0 = off / 1 = on                                          |
         * |         +---------+-----------------------------------------------------------+
         * |         | 6 - 7   | RC switch type.                                           |
         * |         |         | Type B: 01                                                |
         * +---------+---------+-----------------------------------------------------------+
         * |       3 | 0 - 7   | Group id (1 - 4).                                         |
         * |         |         | Ex: 3 --> 0000 0011                                       |
         * +---------+---------+-----------------------------------------------------------+
         * |       4 | 0 - 7   | Device id (1 - 4).                                        |
         * |         |         | Ex: 3 --> 0000 0011                                       |
         * +---------+---------+-----------------------------------------------------------+
         *
         *
         * +-------------------------------------------------------------------------------+
         * | Type C switch                                                                 |
         * +---------+---------+-----------------------------------------------------------+
         * | Byte    | Bits    | Description                                               |
         * +---------+---------+-----------------------------------------------------------+
         * |      1  | 0 - 7   | Command byte: subscribe to RC switch commands.            |
         * |         |         | Decimal value: 111                                        |
         * +---------+---------+-----------------------------------------------------------+
         * |      2  | 0       | Pin on which the 433 MHz receiver module is connected.    |
         * |         |         | 0 -> D2 / 1 -> D3                                         |
         * |         +---------+-----------------------------------------------------------+
         * |         | 1 - 3   | Subscription number                                       |
         * |         |         |                                                           |
         * |         +---------+-----------------------------------------------------------+
         * |         | 4       | Unused                                                    |
         * |         |         |                                                           |
         * |         +---------+-----------------------------------------------------------+
         * |         | 5       | Initial state.                                            |
         * |         |         | 0 = off / 1 = on                                          |
         * |         +---------+-----------------------------------------------------------+
         * |         | 6 - 7   | RC switch type.                                           |
         * |         |         | Type C: 10                                                |
         * +---------+---------+-----------------------------------------------------------+
         * |       3 | 0 - 7   | Device family ('a' - 'f'), as the ASCII code of the       |
         * |         |         | desired letter.                                           |
         * |         |         | Ex: 'b' --> 0110 0001                                     |
         * +---------+---------+-----------------------------------------------------------+
         * |       4 | 0 - 1   | Device id (1 - 4), minus 1.                               |
         * |         |         | Ex: device #3 --> 10                                      |
         * |         +---------+-----------------------------------------------------------+
         * |         | 2 - 3   | Device group (1 - 4), minus 1.                            |
         * |         |         | Ex: group #1 --> 00                                       |
         * |         +---------+-----------------------------------------------------------+
         * |         | 4 - 7   | Unused                                                    |
         * |         |         |                                                           |
         * +---------+---------+-----------------------------------------------------------+
         *
         *
         * +-------------------------------------------------------------------------------+
         * | Type D switch                                                                 |
         * +---------+---------+-----------------------------------------------------------+
         * | Byte    | Bits    | Description                                               |
         * +---------+---------+-----------------------------------------------------------+
         * |      1  | 0 - 7   | Command byte: subscribe to RC switch commands.            |
         * |         |         | Decimal value: 111                                        |
         * +---------+---------+-----------------------------------------------------------+
         * |      2  | 0       | Pin on which the 433 MHz receiver module is connected.    |
         * |         |         | 0 -> D2 / 1 -> D3                                         |
         * |         +---------+-----------------------------------------------------------+
         * |         | 1 - 3   | Subscription number                                       |
         * |         |         |                                                           |
         * |         +---------+-----------------------------------------------------------+
         * |         | 4       | Unused                                                    |
         * |         |         |                                                           |
         * |         +---------+-----------------------------------------------------------+
         * |         | 5       | Initial state.                                            |
         * |         |         | 0 = off / 1 = on                                          |
         * |         +---------+-----------------------------------------------------------+
         * |         | 6 - 7   | RC switch type.                                           |
         * |         |         | Type D: 11                                                |
         * +---------+---------+-----------------------------------------------------------+
         * |       3 | 0 - 7   | Device family ('A' - 'D'), as the ASCII code of the       |
         * |         |         | desired letter.                                           |
         * |         |         | Ex: 'C' --> 0100 0011                                     |
         * +---------+---------+-----------------------------------------------------------+
         * |       4 | 0 - 7   | Device id (1 - 3).                                        |
         * |         |         | Ex: 3 --> 0000 0011                                       |
         * +---------+---------+-----------------------------------------------------------+
         */
		else if (cmd[0]==rc_switch_subscribe_cmd) {
			if (run_once == 1) {// Ensure we do not repeatedly execute this command while waiting for another one

                // Apply bit-mask to recover data from the 2nd command byte
                // pin: bit 0. 0 --> pin 2 / 1 --> pin 3
                pin = 2 + (cmd[1] & 1);

                // subscription number: bits 1-3
                rc_switch_subscription_number = uint8_t(cmd[1] >> 1 & 7);

                // initial state (on/off): bit 5
                rc_switch_state = uint8_t(cmd[1] >> 5 & 1);

                // remote switch type: 4 possible types encoded in bits 6-7
                rc_switch_type = uint8_t(cmd[1] >> 6);

				// Enable radio if it is not already done
                if (!rc_switch_run_bk) {
                    rc_switch.enableReceive(digitalPinToInterrupt(pin));
                    rc_switch_run_bk = true;
                }

                // Handle remaining bytes depending on the switch type
                switch (rc_switch_type) {
                    case rc_switch_typeA: {
                        // For this type of remote controlled switches, the RCSwitch library requires 2 parameters, group and
                        // device, as 5-chars binary strings, padded with zeroes. These parameters should match DIP switches present
                        // on the switch device.
                        // Ex: a DIP switch set as OFF-ON-ON-ON-OFF is represented by the parameter string "01110"

                        // Conversion of the group parameter in the appropriate format
                        for (i = 4; i >= 0; --i) {
                            rc_switch_typeA_group[4 - i] = (cmd[2] & (1 << i) ? '1' : '0');
                        }
                        rc_switch_typeA_group[5] = '\0';

                        // Conversion of the device parameter in the appropriate format
                        for (i = 4; i >= 0; --i) {
                            rc_switch_typeA_device[4 - i] = (cmd[3] & (1 << i) ? '1' : '0');
                        }
                        rc_switch_typeA_device[5] = '\0';

                        // Store subscription
                        rc_switch_subscription[rc_switch_subscription_number].offCode =
                                rc_switch.switchOffCode(rc_switch_typeA_group, rc_switch_typeA_device);
                        rc_switch_subscription[rc_switch_subscription_number].onCode =
                                rc_switch.switchOnCode(rc_switch_typeA_group, rc_switch_typeA_device);
                        rc_switch_subscription[rc_switch_subscription_number].lastStatus = rc_switch_state;

                        break;
                    }
                    case rc_switch_typeB: {
                        // For this type of remote controlled switches, the RCSwitch library requires two parameters:
                        // group as an int [1..4] --> directly passed in 3rd byte cmd[2]
                        // device as an int [1..4] --> directly passed in 4th byte cmd[3]

                        // Store subscription
                        rc_switch_subscription[rc_switch_subscription_number].offCode =
                                rc_switch.switchOffCode(cmd[2], cmd[3]);
                        rc_switch_subscription[rc_switch_subscription_number].onCode =
                                rc_switch.switchOnCode(cmd[2], cmd[3]);

						rc_switch_subscription[rc_switch_subscription_number].lastStatus = rc_switch_state;
						break;
                    }
                    case rc_switch_typeC: {
                        // For this type of remote controlled switches, the RCSwitch library requires three parameters:
                        // family code as a char ['a'..'f'] --> directly passed in 3rd byte cmd[2]
                        // group as int [1..4] --> this value minus one is passed using bits 2 and 3 of the 4th byte cmd[3]
                        // device as int [1..4] --> this value minus one is passed using bits 0 and 1 of the 4th byte cmd[3]

                        // Store subscription
                        rc_switch_subscription[rc_switch_subscription_number].offCode =
                                rc_switch.switchOffCode(char(cmd[2]), 1 + (cmd[3] >> 2 & 3), 1 + (cmd[3] & 3));
                        rc_switch_subscription[rc_switch_subscription_number].onCode =
                                rc_switch.switchOnCode(char(cmd[2]), 1 + (cmd[3] >> 2 & 3), 1 + (cmd[3] & 3));
                        rc_switch_subscription[rc_switch_subscription_number].lastStatus = rc_switch_state;
                        break;
                    }
                    case rc_switch_typeD: {
                        // For this type of remote controlled switches, the RCSwitch library requires two parameters:
                        // group as a char ['A'..'D'] --> directly passed in 3rd byte cmd[2]
                        // device as an int [1..3] --> directly passed in 4th byte cmd[3]

                        // Store subscription
                        rc_switch_subscription[rc_switch_subscription_number].offCode =
                                rc_switch.switchOffCode(char(cmd[2]), cmd[3]);
                        rc_switch_subscription[rc_switch_subscription_number].onCode =
                                rc_switch.switchOnCode(char(cmd[2]), cmd[3]);
                        rc_switch_subscription[rc_switch_subscription_number].lastStatus = rc_switch_state;
                        break;
                    }
                    default: {
                        // Unknown switch type --> do nothing
                    }

                }
			}
			cmd[0] = 0;
			run_once = 0;
		}
        /* Command 112 - 433MHz receiver: read last status
         *
         * Retrieve last received command for a subscription slot
         *
         * +---------+---------+-----------------------------------------------------------+
         * | Byte    | Bits    | Description                                               |
         * +---------+---------+-----------------------------------------------------------+
         * |      1  | 0 - 7   | Command byte: subscribe to RC switch commands.            |
         * |         |         | Decimal value: 112                                        |
         * +---------+---------+-----------------------------------------------------------+
         * |      2  | 0       | Unused                                                    |
         * |         |         |                                                           |
         * |         +---------+-----------------------------------------------------------+
         * |         | 1 - 3   | Subscription number                                       |
         * |         |         |                                                           |
         * |         +---------+-----------------------------------------------------------+
         * |         | 4 - 7   | Unused                                                    |
         * |         |         |                                                           |
         * +---------+---------+-----------------------------------------------------------+
         * |       3 | 0 - 7   | Unused                                                    |
         * |         |         |                                                           |
         * +---------+---------+-----------------------------------------------------------+
         * |       4 | 0 - 7   | Unused                                                    |
         * |         |         |                                                           |
         * +---------+---------+-----------------------------------------------------------+
         */
        else if (cmd[0]==rc_switch_read_cmd) {
			if (run_once == 1) { // Ensure we do not repeatedly execute this command while waiting for another one

                // Apply bit-mask to recover data from the 2nd command byte
                // subscription number: bits 1-3
                rc_switch_subscription_number = uint8_t(cmd[1] >> 1 & 7);
                val = rc_switch_subscription[rc_switch_subscription_number].lastStatus;
            }
			run_once = 0;
		}
	}
    //Dust sensor can run in background so has a dedicated if condition
    if(dust_run_bk)
    {
		if(millis()-starttime>30000)
		{
			dust_latest=1;
			latest_dust_val=lowpulseoccupancy;
			lowpulseoccupancy=0;
			starttime=millis();
		}
    }

    if(enc_run_bk)
    {
        if (encoder.rotate_flag ==1)
        {
            if (encoder.direct==1)
            {
                index_LED++;
                if (index_LED>24)
                index_LED=0;
                enc_val[0]=1;
                enc_val[1]=index_LED;
            }
            else
            {
                index_LED--;
                if(index_LED<0)
                index_LED=24;
                enc_val[0]=1;
                enc_val[1]=index_LED;
            }
            encoder.rotate_flag =0;
        }
    }

    if(flow_run_bk)
    {
        if(millis()-flow_read_start>2000)
        {
            Calc = (NbTopsFan * 30 / 73);
            flow_val[0]=1;
            flow_val[1]=Calc%256;
            flow_val[2]=Calc/256;
            NbTopsFan = 0;
            flow_read_start=millis();
        }
    }

	if(rc_switch_run_bk)
	{
		// Check if we have received a radio command
		if (rc_switch.available())
		{
			// Check if we have to update one of our subscriptions
			for (j = 0; j < rc_switch_max_sub; j++) {
				if (rc_switch_subscription[j].offCode == rc_switch.getReceivedValue()) {
					rc_switch_subscription[j].lastStatus = 0;
				} else if (rc_switch_subscription[j].onCode == rc_switch.getReceivedValue()) {
					rc_switch_subscription[j].lastStatus = 1;
				}
			}
			rc_switch.resetAvailable();
		}
	}
}

void receiveData(int byteCount)
{
    while(Wire.available())
    {
      if(Wire.available()==4)
      {
        flag=0; 
        index=0;
		run_once=1;
      }
        cmd[index++] = Wire.read();
    }
}

// callback for sending data
void sendData()
{
  if(cmd[0] == 1)
    Wire.write(val);
  if(cmd[0] == 3 || cmd[0] == 7 || cmd[0] == 56)
    Wire.write(b, 3);
  if(cmd[0] == 8 || cmd[0] == 20)
    Wire.write(b, 4);
  if(cmd[0] == 30) 
    Wire.write(b, 9);
  if(cmd[0] == 40) 
    Wire.write(dht_b, 9);
  
  if(cmd[0]==21)
  {
    Wire.write(b,21);     
    b[0]=0;
  }
  if(cmd[0]==dust_sensor_read_cmd)
  {
    Wire.write(b,4);     
	dust_latest=0;
	cmd[0]=0;
  }
  if(cmd[0]==encoder_read_cmd)
  {
    Wire.write(enc_val,2);     
    enc_val[0]=0;
	cmd[0]=0;
  }
  if(cmd[0]==flow_read_cmd)
  {
    Wire.write(flow_val,3);     
    flow_val[0]=0;
	cmd[0]=0;
  }
  if(cmd[0]==rc_switch_read_cmd)
  {
    Wire.write(val);
    cmd[0]=0;
  }
  
}

//ISR for the flow sensor
void rpm ()     //This is the function that the interupt calls 
{ 
  NbTopsFan++;  //This function measures the rising and falling edge of the 
 
//hall effect sensors signal
} 

void readPulseDust()
{
  t = millis();
  l_status = digitalRead(2);  // Represents if the line is low or high.  
  if(l_status)
  { 
	 digitalWrite(8,0);
    // If the line is high (1), the pulse just ended
    pulse_end = t;
  }
  else
  {   // If the line is low (0), the pulse just started
    pulse_start = t;
	digitalWrite(8,1);
  }
  
  if(pulse_end > pulse_start)
  {
    duration = pulse_end - pulse_start;
    lowpulseoccupancy = lowpulseoccupancy+duration;   // Add to the pulse length.
    pulse_end = 0;    // If you don't reset this, you'll keep adding the pulse length over and over.
  }
}
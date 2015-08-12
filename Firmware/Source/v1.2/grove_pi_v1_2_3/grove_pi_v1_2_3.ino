#include <Wire.h>
#include "MMA7660.h"
#include "DS1307.h"
#include "DHT.h"
#include "Grove_LED_Bar.h"
#include "TM1637.h"
#include "ChainableLED.h"
#include "IRSendRev.h"
#include "TinyGPS.h"

MMA7660 acc;
DS1307 clock;
DHT dht;
Grove_LED_Bar ledbar[6];  // 7 instances for D2-D8, however, max 4 bars, you can't use adjacent sockets, 4 pin display
TM1637 fourdigit[6];      // 7 instances for D2-D8, however, max 4 displays, you can't use adjacent sockets, 4 pin display
ChainableLED rgbled[6];   // 7 instances for D2-D8
TinyGPSPlus gps;

#define SLAVE_ADDRESS 0x04

int cmd[5];
int index=0;
int flag=0;
int i;
byte val=0,b[21],float_array[4];
unsigned char dta[21];
int length;
int aRead=0;
byte accFlag=0,clkFlag=0;
int8_t accv[3];
byte rgb[] = { 0, 0, 0 };
void setup()
{
    Serial.begin(9600);         // start serial for output
    Wire.begin(SLAVE_ADDRESS);

    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);
    // IR.Init(8);
    // Serial.println("Ready!");
}
int pin;
int j;
void loop()
{
  long dur,RangeCm;
  if(index==4)
  {
    flag=1;
    //IR reciever pin set command
    if(cmd[0]==22)
       IR.Init(cmd[1]);
    
    //Grove IR recieve command
    if(cmd[0]==21)
    {
        if(IR.IsDta())
        {
            int length= IR.Recv(dta);
            b[0]=1;
            for(i=0;i<20;i++) 
                b[i+1]=dta[i];
        }
    }
    
    //Digital Read
    if(cmd[0]==1)
      val=digitalRead(cmd[1]);

    //Digital Write
    if(cmd[0]==2)
      digitalWrite(cmd[1],cmd[2]);

    //Analog Read
    if(cmd[0]==3)
    {
      aRead=analogRead(cmd[1]);
      b[1]=aRead/256;
      b[2]=aRead%256;
    }

    //Set up Analog Write
    if(cmd[0]==4)
      analogWrite(cmd[1],cmd[2]);

    //Set up pinMode
    if(cmd[0]==5)
      pinMode(cmd[1],cmd[2]);

    //Ultrasonic Read
    if(cmd[0]==7)
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
    if(cmd[0]==8)
    {
      b[1] = 1;
      b[2] = 2;
      b[3] = 3;
    }
    
    //GPS running on Arduino Serial port
    if(cmd[0]==11)
    {
      if (gps.location.isValid()) {
        float lat = gps.location.lat() ;
        float lng = gps.location.lng() ;
        float alt = gps.altitude.meters();
        byte *b1=(byte*)&lat;
        byte *b2=(byte*)&lng;
        byte *b3=(byte*)&alt;
        for(j=0;j<4;j++)
          b[j+1]=b1[j];
        for(j=4;j<8;j++)
          b[j+1]=b2[j-4];
        for(j=8;j<12;j++)
          b[j+1]=b2[j-8];
      }
      if(gps.time.isValid())
      {
        int year = gps.date.year();
        byte *b4=(byte*)&year;
        b[13]=b4[0];
        b[14]=b4[1];
        b[15]=gps.date.month();
        b[16]=gps.date.day();
        b[17]=gps.time.hour();
        b[18]=gps.time.minute();
        b[19]=gps.time.second();
        b[20]=gps.time.centisecond();
      }
    }
    
    //Accelerometer x,y,z, read
    if(cmd[0]==20)
    {
      if(accFlag==0)
      {
        acc.init();
        accFlag=1;
      }
      acc.getXYZ(&accv[0],&accv[1],&accv[2]);
      b[1]=accv[0];
      b[2]=accv[1];
      b[3]=accv[2];
    }
    //RTC tine read
    if(cmd[0]==30)
    {
      if(clkFlag==0)
      {
        clock.begin();
        //Set time the first time
        //clock.fillByYMD(2013,1,19);
        //clock.fillByHMS(15,28,30);//15:28 30"
        //clock.fillDayOfWeek(SAT);//Saturday
        //clock.setTime();//write time to the RTC chip
        clkFlag=1;
      }
      clock.getTime();
      b[1]=clock.hour;
      b[2]=clock.minute;
      b[3]=clock.second;
      b[4]=clock.month;
      b[5]=clock.dayOfMonth;
      b[6]=clock.year;
      b[7]=clock.dayOfMonth;
      b[8]=clock.dayOfWeek;
    }
    //Grove temp and humidity sensor pro
    //40- Temperature
    if(cmd[0]==40)
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
        b[j+1]=b1[j];
      for(j=4;j<8;j++)
        b[j+1]=b2[j-4];
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
    if(cmd[0] == 50)
    {
      // clock pin is always next to the data pin
      ledbar[cmd[1]-2].begin(cmd[1]+1, cmd[1], cmd[2]); // clock, data, orientation
    }

    // Change the orientation
    // Green to red, or red to green
    // [51, pin, greenToRed, unused]
    if(cmd[0] == 51 && ledbar[cmd[1]-2].ready())
    {
      ledbar[cmd[1]-2].setGreenToRed(cmd[2]);
    }

    // Set level (0-10)
    // Level 0 means all leds off
    // Level 10 means all leds on
    // [52, pin, level, unused]
    if(cmd[0] == 52 && ledbar[cmd[1]-2].ready())
    {
      ledbar[cmd[1]-2].setLevel(cmd[2]);
    }

    // Set a single led
    // led (1-10)
    // state (0=off, 1=on)
    // [53, pin, led, state]
    if(cmd[0] == 53 && ledbar[cmd[1]-2].ready())
    {
      ledbar[cmd[1]-2].setLed(cmd[2], cmd[3]);
    }

    // Toggle a single led
    // led (1-10)
    // [54, pin, led, unused]
    if(cmd[0] == 54 && ledbar[cmd[1]-2].ready())
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
    if(cmd[0] == 55 && ledbar[cmd[1]-2].ready())
    {
      ledbar[cmd[1]-2].setBits(cmd[2] ^ (cmd[3] << 8));
    }

    // Return the current state
    // [56, pin, unused, unused]
    if(cmd[0] == 56 && ledbar[cmd[1]-2].ready())
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
    if(cmd[0] == 70)
    {
      // clock pin is always next to the data pin
      fourdigit[cmd[1]-2].begin(cmd[1], cmd[1]+1);  // clock, data
    }

    // set brightness
    // [71, pin, brightness, unused]
    if(cmd[0] == 71 && fourdigit[cmd[1]-2].ready())
    {
      fourdigit[cmd[1]-2].setBrightness(cmd[2]);  // setBrightness(brightness)
    }

    // show right aligned decimal value without leading zeros
    // [72, pin, bits 1-8, bits 9-16]
    if(cmd[0] == 72 && fourdigit[cmd[1]-2].ready())
    {
      fourdigit[cmd[1]-2].showNumberDec(cmd[2] ^ (cmd[3] << 8), false);  // showNumberDec(number, leading_zero)
    }

    // show right aligned decimal value with leading zeros
    // [73, pin, bits 1-8, bits 9-16]
    if(cmd[0] == 73 && fourdigit[cmd[1]-2].ready())
    {
      fourdigit[cmd[1]-2].showNumberDec(cmd[2] ^ (cmd[3] << 8), true);  // showNumberDec(number, leading_zero)
    }

    // set individual digit
    // [74, pin, index, dec]
    if(cmd[0] == 74 && fourdigit[cmd[1]-2].ready())
    {
      uint8_t data[] = {};
      data[0] = fourdigit[cmd[1]-2].encodeDigit(cmd[3]);  // encodeDigit(number)
      fourdigit[cmd[1]-2].setSegments(data, 1, cmd[2]);  // setSegments(segments[], length, position)
    }

    // set individual segment
    // [75, pin, index, binary]
    if(cmd[0] == 75 && fourdigit[cmd[1]-2].ready())
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
    if(cmd[0] == 76 && fourdigit[cmd[1]-2].ready())
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
    if(cmd[0] == 77 && fourdigit[cmd[1]-2].ready())
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
    if(cmd[0] == 78 && fourdigit[cmd[1]-2].ready())
    {
      uint8_t data[] = { 0xFF, 0xFF, 0xFF, 0xFF };
      fourdigit[cmd[1]-2].setSegments(data, 4, 0);  // setSegments(segments[], length, position)
    }

    // display off
    // [79, pin, unused, unused]
    if(cmd[0] == 79 && fourdigit[cmd[1]-2].ready())
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
    if(cmd[0] == 90)
    {
      rgb[0] = cmd[1];
      rgb[1] = cmd[2];
      rgb[2] = cmd[3];
    }

    // Initialise a RGB LED chain
    // [91, pin, num leds, unused]
    if(cmd[0] == 91)
    {
      rgbled[cmd[1]-2].begin(cmd[1], cmd[1]+1, cmd[2]);  // clock, data, num leds
    }
    
    // Test colors, repeating red green blue
    // color code: 0 black (off), 1 blue, 2 green, 3 cyan, 4 red, 5 magenta, 6 yellow, 7 white
    // [92, pin, num leds, color code]
    if(cmd[0] == 92)
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
    if(cmd[0] == 93)
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
    if(cmd[0] == 94)
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
    if(cmd[0] == 95)
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

    // end Grove Chainable RGB LED 
    
    // GPS background polling
    if(Serial.available() > 0) {
      gps.encode(Serial.read());   
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
  if(cmd[0] == 11)
    Wire.write(b, 21);
  if(cmd[0] == 30 || cmd[0] == 40)
    Wire.write(b, 9);
  if(cmd[0]==21)
  {
    Wire.write(b,21);     
    b[0]=0;
  }
}


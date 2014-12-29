#include <Wire.h>
#include "MMA7660.h"
#include "DS1307.h"
#include "DHT.h"
#include "Grove_LED_bar.h"
MMA7660 acc;
DS1307 clock;
DHT dht;
Grove_LED_Bar ledbar[6];  // 7 instances for D2-D8, however, max 4 bars, you can't use adjacent sockets, 4 pin sensor

#define SLAVE_ADDRESS 0x04
int number = 0;
int state = 0;

int cmd[5];
int index=0;
int flag=0;
int i;
byte val=0,b[9],float_array[4];
int aRead=0;
byte accFlag=0,clkFlag=0;
int8_t accv[3];
void setup() 
{
    Serial.begin(9600);         // start serial for output
    Wire.begin(SLAVE_ADDRESS);

    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);

    Serial.println("Ready!");
}
int pin;
int j;
void loop()
{
  long dur,RangeCm;
  if(index==4 && flag==0)
  {
    flag=1;
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
      b[3] = 0;
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
    
    // LED Bar
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
    
    // end LED Bar
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
  if(cmd[0] == 30 || cmd[0] == 40)
    Wire.write(b, 9);
}


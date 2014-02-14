#include <Wire.h>
#include <Servo.h>

Servo myservo;  // 
#define SLAVE_ADDRESS 0x04
int number = 0;
int state = 0;

int cmd[5];
int index=0;
int flag=0;
int i;
byte val=0,b[3];
int aRead=0;
int pos;
void setup() {
    pinMode(13, OUTPUT);
    //Serial.begin(9600);         // start serial for output

    Wire.begin(SLAVE_ADDRESS);

    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);

    //Serial.println("Ready!");
    pinMode(4,OUTPUT);
     myservo.attach(5); 
}

void loop()
{
  if(flag==1)
  {
   for(pos = 0; pos < 180; pos += 1)  // goes from 0 degrees to 180 degrees 
  {                                  // in steps of 1 degree 
    myservo.write(pos);              // tell servo to go to position in variable 'pos' 
    delay(15);                       // waits 15ms for the servo to reach the position 
  } 
  for(pos = 180; pos>=1; pos-=1)     // goes from 180 degrees to 0 degrees 
  {                                
    myservo.write(pos);              // tell servo to go to position in variable 'pos' 
    delay(15);                       // waits 15ms for the servo to reach the position 
  } 
  }
}


void receiveData(int byteCount)
{
  flag=1;
    while(Wire.available()) 
    {
      if(Wire.available()==4)
      { 
       
        index=0;
      }
        cmd[index++] = Wire.read();
    }
}

// callback for sending data
void sendData()
{
  if(cmd[0]==1)
    Wire.write(val);
  if(cmd[0]==3)
    Wire.write(b, 3);
}


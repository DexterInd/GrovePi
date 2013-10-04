#include <Wire.h>

#define SLAVE_ADDRESS 0x04
int number = 0;
int state = 0;

int cmd[5];
int index=0;
int flag=0;
int i;
byte val=0,b[3];
int aRead=0;

void setup() {
    pinMode(13, OUTPUT);
    //Serial.begin(9600);         // start serial for output

    Wire.begin(SLAVE_ADDRESS);

    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);

    //Serial.println("Ready!");
    pinMode(4,OUTPUT);
}

void loop()
{
  
  //digitalWrite(4,1);
  if(index==4 && flag==0)
  {
    /*for(i=0;i<4;i++)
    {
      Serial.print(" ");
      Serial.print(cmd[i]);
    }
    Serial.println();
    */
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
        //Serial.print("data received: ");
    }
}

// callback for sending data
void sendData()
{
  if(cmd[0]==1)
  {
    //Serial.println("dr");
    Wire.write(val);
  }
  if(cmd[0]==3)
  {
    //Serial.println("ar");
    Wire.write(b, 3);
  }
}


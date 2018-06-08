#include <Wire.h>
#include "DHT.h"
#include "Grove_LED_Bar.h"
#include "TM1637.h"
#include "ChainableLED.h"
#include "Encoder.h"
#include "TimerOne.h"
#include "Queue.h"

#define SLAVE_ADDRESS 0x04
#define MAX_PAYLOAD 10

struct Request{
  uint8_t command_id;
  uint8_t no_bytes;
  uint8_t payload[MAX_PAYLOAD];
};

Queue<Request> requests = Queue<Request>(15);
Request new_request;
Request temp_request;
uint8_t receive_counter = 0;
uint8_t main_counter = 0;

void flushI2C();

void setup()
{
    Serial.begin(38400); // start serial for output

    Wire.begin(SLAVE_ADDRESS);
    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);
}

void loop()
{
  if(requests.count() > 0)
  {
    temp_request = requests.pop();
    Serial.print("CID=" + String(temp_request.command_id) + "+Bytes=" + String(temp_request.no_bytes) + "+List=");
    main_counter = 0;
    while(main_counter < temp_request.no_bytes)
    {
      Serial.print("" + String(temp_request.payload[main_counter]));
      main_counter++;
    }
    Serial.println();
  }
}

void receiveData(int byteCount)
{
  if(byteCount >= 2)
  {
    new_request.command_id = Wire.read();
    new_request.no_bytes = Wire.read();
    byteCount -= 2;
  }
  else
  {
    flushI2C();
    return;
  }

  if(byteCount == new_request.no_bytes)
  {
    receive_counter = 0;
    while(receive_counter < byteCount)
      new_request.payload[receive_counter++] = Wire.read();
  }
  else{
    flushI2C();
    return;
  }

  requests.push(new_request);
}

void sendData()
{
  Serial.println("on send");
}

void flushI2C()
{
  while(Wire.available() > 0)
    Wire.read();
}

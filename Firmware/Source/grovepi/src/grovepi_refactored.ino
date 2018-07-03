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

  Request& operator=(const Request &d)
  {
    this->command_id = d.command_id;
    this->no_bytes = d.no_bytes;
    for(uint8_t i = 0; i < this->no_bytes; i++)
      this->payload[i] = d.payload[i];

    return *this;
  }
};

Request request;
Request temp_request;
uint8_t receive_counter = 0;
uint8_t main_counter = 0;
bool busy_loop = false;
bool new_request = false;

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
  if(new_request == true)
  {
    busy_loop = true;

    temp_request = request;
    Serial.print("CID=" + String(temp_request.command_id) + "+Bytes=" + String(temp_request.no_bytes) + "+List=");
    main_counter = 0;
    while(main_counter < temp_request.no_bytes)
    {
      Serial.print("" + String(temp_request.payload[main_counter]));
      main_counter++;
    }
    Serial.println();

    new_request = false;
    busy_loop = false;
  }
}

void receiveData(int byteCount)
{
  // discard any incoming data if the main loop is busy
  if(busy_loop == true) flushI2C();
  else
  {
    if(byteCount >= 2)
    {
      request.command_id = Wire.read();
      request.no_bytes = Wire.read();
      byteCount -= 2;

      if(byteCount == request.no_bytes)
      {
        receive_counter = 0;
        while(receive_counter < byteCount)
        {
          request.payload[receive_counter] = Wire.read();
          receive_counter++;
        }
        new_request = true;
      }
      else flushI2C();
    }
    else flushI2C();
  }
}

void sendData()
{
  Serial.println("on send");
}

void flushI2C()
{
  while(Wire.available())
    Wire.read();
}

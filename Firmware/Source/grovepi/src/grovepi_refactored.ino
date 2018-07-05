// #include <Wire.h>
// #include "DHT.h"
// #include "Grove_LED_Bar.h"
// #include "TM1637.h"
// #include "ChainableLED.h"
// #include "Encoder.h"
// #include "TimerOne.h"
// #include "Queue.h"
//
// #define SLAVE_ADDRESS 0x04
// #define MAX_PAYLOAD 10
//
// enum Command : uint8_t {
//   DIGITALREAD = 1,
//   DIGITALWRITE = 2,
//   ANALOGREAD = 3,
//   ANALOGWRITE = 4,
//   PINMODE = 5,
//   ULTRASONICREAD = 7,
//   VERSION = 8,
//
//   DUSTSENSOR_READ = 10,
//   DUSTSENSOR_EN = 14,
//   DUSTSENSOR_DIS = 15,
//   ENCODER_READ = 11,
//   ENCODER_EN = 16,
//   ENCODER_DIS = 17,
//   FLOW_READ = 12,
//   FLOW_EN = 18,
//   FLOW_DIS = 13,
//   IR_READ = 21,
//   IR_SET_PIN = 22,
//
//   ACC_XYZ = 20,
//   RTC_GETTIME = 30,
//   DHT_TEMP = 40,
//
//   LEDBAR_INIT = 50,
//   LEDBAR_ORIENT = 51,
//   LEDBAR_LEVEL = 52,
//   LEDBAR_SETTONE = 53,
//   LEDBAR_TOGGLEONE = 54,
//   LEDBAR_SETALL = 55,
//   LEDBAR_GETALL = 56,
//
//   F4DIGIT_INIT = 70,
//   F4DIGIT_SET_BRIGHTNESS = 71,
//   F4DIGIT_VALUE_SET = 72,
//   F4DIGIT_VALUE_SET_WZEROS = 73,
//   F4DIGIT_INDIVID_DIGITS = 74,
//   F4DIGIT_INDIVID_LEDS = 75,
//   F4DIGIT_SCORE = 76,
//   F4DIGIT_ANALOGREAD_SECONDS = 77,
//   F4DIGIT_ALLON = 78,
//   F4DIGIT_ALLOFF = 79,
//
//   STORE_COLOR = 90,
//   CHAINRGB_INIT = 91,
//   CHAINRGB_TEST = 92,
//   CHAINRGB_SET_PATTN = 93,
//   CHAINRGB_SET_MOD = 94,
//   CHAINRGB_SET_LVL = 95
// };
//
// struct Request{
//   uint8_t command_id;
//   uint8_t no_bytes;
//   uint8_t payload[MAX_PAYLOAD];
//
//   Request& operator=(const Request &d)
//   {
//     this->command_id = d.command_id;
//     this->no_bytes = d.no_bytes;
//     for(uint8_t i = 0; i < this->no_bytes; i++)
//       this->payload[i] = d.payload[i];
//
//     return *this;
//   }
// };
//
// volatile Request request, response;
// uint8_t main_counter = 0;
// volatile uint8_t receive_counter = 0, send_counter = 0;
// volatile bool busy_loop = false;
// volatile bool new_request = false;
// volatile bool new_response = false;
// bool stage_response = false;
//
// uint8_t pin;
// uint8_t value8;
// uint16_t value16;
//
// void flushI2C();
//
// void setup()
// {
//     Serial.begin(38400); // start serial for output
//
//     Wire.begin(SLAVE_ADDRESS);
//     Wire.onReceive(receiveData);
//     Wire.onRequest(sendData);
// }
//
// void loop()
// {
//   if(new_request == true)
//   {
//     busy_loop = true;
//     new_response = false;
//
//     Serial.print("CID=" + String(request.command_id) + "+Bytes=" + String(request.no_bytes) + "+List=");
//     main_counter = 0;
//     while(main_counter < request.no_bytes)
//     {
//       Serial.print("" + String(request.payload[main_counter]));
//       main_counter++;
//     }
//     Serial.println();
//
//     stage_response = false;
//     response.command_id = request.command_id;
//     switch(request.command_id)
//     {
//       case DIGITALREAD:
//         response.no_bytes = 1;
//         response.payload[0] = digitalRead(request.payload[0]);
//         stage_response = true;
//         break;
//       case DIGITALWRITE:
//         pin = request.payload[0];
//         value8 = request.payload[1];
//         digitalWrite(pin, value8);
//         break;
//       case ANALOGREAD:
//         response.no_bytes = 2;
//         value16 = analogRead(request.payload[0]);
//         response.payload[0] = value16 >> 8;
//         response.payload[1] = value16 & 0xFF;
//         stage_response = true;
//         break;
//       case ANALOGWRITE:
//         pin = request.payload[0];
//         value8 = request.payload[1];
//         analogWrite(pin, value8);
//         break;
//     }
//
//     new_request = false;
//     busy_loop = false;
//     new_response = stage_response;
//   }
// }
//
// void receiveData(int byteCount)
// {
//   // discard any incoming data if the main loop is busy
//   if(busy_loop == true) flushI2C();
//   else
//   {
//     if(byteCount >= 2)
//     {
//       request.command_id = Wire.read();
//       request.no_bytes = Wire.read();
//       byteCount -= 2;
//
//       if(byteCount == request.no_bytes)
//       {
//         receive_counter = 0;
//         while(receive_counter < byteCount)
//         {
//           request.payload[receive_counter] = Wire.read();
//           receive_counter++;
//         }
//         new_request = true;
//       }
//       else flushI2C();
//     }
//     else flushI2C();
//   }
// }
// 
// void sendData()
// {
//   if(new_response == true)
//   {
//     Wire.write(response.command_id);
//     Wire.write(response.no_bytes);
//     send_counter = 0;
//     while(send_counter < response.no_bytes)
//     {
//       Wire.write(response.payload[send_counter]);
//       send_counter++;
//     }
//
//     new_response = false;
//   }
// }
//
// void flushI2C()
// {
//   while(Wire.available())
//     Wire.read();
// }

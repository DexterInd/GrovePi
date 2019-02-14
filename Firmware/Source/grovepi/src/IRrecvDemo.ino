// /*
//  * IRremote: IRrecvDemo - demonstrates receiving IR codes with IRrecv
//  * An IR detector/demodulator must be connected to the input RECV_PIN.
//  * Version 0.1 July, 2009
//  * Copyright 2009 Ken Shirriff
//  * http://arcfn.com
//  */
//
// #include <IRremote.h>
//
// int RECV_PIN = 3;
// int BLINK_PIN = 2;
//
// IRrecv irrecv(RECV_PIN, BLINK_PIN);
//
// decode_results results;
//
// void setup()
// {
//   Serial.begin(9600);
//   // In case the interrupt driver crashes on setup, give a clue
//   // to the user what's going on.
//   Serial.println("Enabling IRin");
//   irrecv.enableIRIn(); // Start the receiver
//   Serial.println("Enabled IRin");
// }
//
// void loop() {
//   if (irrecv.decode(&results)) {
//     Serial.print(results.decode_type);
//     Serial.print(" ");
//     Serial.print(results.address, HEX);
//     Serial.print(" ");
//     Serial.println(results.value, HEX);
//     irrecv.resume(); // Receive the next value
//   }
//   delay(100);
// }

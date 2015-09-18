/*
 2012 Copyright (c) Seeed Technology Inc.

 Author: LG
  
 This library is free software; you can redistribute it and/or
 modify it under the terms of the GNU Lesser General Public
 License as published by the Free Software Foundation; either
 version 2.1 of the License, or (at your option) any later version.

 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public
 License along with this library; if not, write to the Free Software
 Foundation, Inc.,51 Franklin St,Fifth Floor, Boston, MA 02110-1301 USA

*/
#include"Encoder.h"
#include<Arduino.h>
#include"TimerOne.h"
//TimerOne Timer1;
char ready_msg=0; 
//char direct_f=0;
//char direct_b=0;
void timerIsr();
Encoder::Encoder()
{
  //set to input and open the interruput
  PCICR=0x04;//enable PCINT[23:16]
  PCIFR&=0x011;//Clear PCINT[23:16] flag bit
  PCMSK2=0x0C;
}
void Encoder::Timer_init(void)
{
    Timer1.initialize(1000); // set a timer of length 100 microseconds
    Timer1.attachInterrupt(timerIsr); // attach the service routine here
    sei();
}
void Encoder::Timer_disable(void)
{
    Timer1.detachInterrupt();
}

ISR(PCINT2_vect)
{
// Serial.println("interrupted1");
  if(ready_msg==1)
	  {
  //Serial.println("interrupted2");
	    if(digitalRead(2) > digitalRead(3))
	    {
	      encoder.direct=1;//adjust direction forward
	     // encoder.direct_b=0;//adjust direction backward
		//		if(count == 24)count = 24;
		//		else count ++;
		//		flag_debug = 1;
                               encoder.rotate_flag =1;
		//		counter_100us = 0;
	      ready_msg=0;
				
	    }
	    else if(digitalRead(2)<digitalRead(3))
	    {
	      encoder.direct=0;//adjust direction forward
	     // encoder.direct_b=1;//adjust direction backward
	      //flag_debug = 1;
                encoder.rotate_flag =1;
	    //  if(count == 0)count = 0;
	     // else count --;
		//		counter_100us = 0;
	      ready_msg=0;
	    }
	    else;
	  }
	//  else
	//  {
	//    delayMicroseconds(200);
	//    if(((digitalRead(2)&digitalRead(3))==1))
	//      ready_msg=1;
	//    else
	//      ready_msg=0;
	//  }
}
void timerIsr()
{
	if((digitalRead(2)&digitalRead(3))==1)
        ready_msg=1;
//	if(counter_100us == 30)
//	{
//		flag_3ms = 1;
//	}
}
Encoder encoder;

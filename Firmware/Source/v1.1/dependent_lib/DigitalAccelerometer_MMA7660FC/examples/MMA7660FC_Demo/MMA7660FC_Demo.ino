/*****************************************************************************/
//    Function:    Get the acc of the x/y/z axis.
//  Hardware:    Grove - 3-Axis Digital Accelerometer(±1.5g)
//    Arduino IDE: Arduino-1.0
//    Author:     Frankie.Chu
//    Date:      Jan 10,2013
//    Version: v0.9b
//    by www.seeedstudio.com


//  modify by loovee
//  2013-9-25
//  add time out
//
//  This library is free software; you can redistribute it and/or
//  modify it under the terms of the GNU Lesser General Public
//  License as published by the Free Software Foundation; either
//  version 2.1 of the License, or (at your option) any later version.
//
//  This library is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
//  Lesser General Public License for more details.
//
//  You should have received a copy of the GNU Lesser General Public
//  License along with this library; if not, write to the Free Software
//  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
//
/*******************************************************************************/

#include <Wire.h>
#include "MMA7660.h"
MMA7660 acc;

void setup()
{
    acc.init();
    pinMode(13, OUTPUT);
    Serial.begin(115200);
}

void loop()
{

    static long cnt     = 0;
    static long cntout  = 0;
    float ax,ay,az;
    int8_t x, y, z;

    acc.getXYZ(&x,&y,&z);

    Serial.print("x = ");
    Serial.println(x);
    Serial.print("y = ");
    Serial.println(y);
    Serial.print("z = ");
    Serial.println(z);


    if(acc.getAcceleration(&ax,&ay,&az))
    {
        Serial.print("get data ok: ");
    }
    else
    {
        Serial.print("tiem out: ");
    }
    
    Serial.println("accleration of X/Y/Z: ");
    Serial.print(ax);
    Serial.println(" g");
    Serial.print(ay);
    Serial.println(" g");
    Serial.print(az);
    Serial.println(" g");
    Serial.println();
    delay(50);

}



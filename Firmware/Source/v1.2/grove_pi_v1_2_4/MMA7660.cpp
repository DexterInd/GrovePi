/*****************************************************************************/
//    Function:     Cpp file for class MMC7660
//  Hardware:    Grove - 3-Axis Digital Accelerometer(±1.5g)
//    Arduino IDE: Arduino-1.0
//    Author:     Frankie.Chu
//    Date:      Jan 10,2013
//    Version: v0.9b
//    by www.seeedstudio.com
//
//  modify by loovee
//  2013-9-25
//  add time out funtion in getXYZ
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
#include <Arduino.h>
#include "MMA7660.h"
/*Function: Write a byte to the register of the MMA7660*/
void MMA7660::write(uint8_t _register, uint8_t _data)
{
    Wire.begin();
    Wire.beginTransmission(MMA7660_ADDR);
    Wire.write(_register);
    Wire.write(_data);
    Wire.endTransmission();
}
/*Function: Read a byte from the regitster of the MMA7660*/
uint8_t MMA7660::read(uint8_t _register)
{
    uint8_t data_read;
    Wire.begin();
    Wire.beginTransmission(MMA7660_ADDR);
    Wire.write(_register);
    Wire.endTransmission();
    Wire.beginTransmission(MMA7660_ADDR);
    Wire.requestFrom(MMA7660_ADDR,1);
    while(Wire.available())
    {
        data_read = Wire.read();
    }
    Wire.endTransmission();
    return data_read;
}

void MMA7660::init()
{
    setMode(MMA7660_STAND_BY);
    setSampleRate(AUTO_SLEEP_120);
    setMode(MMA7660_ACTIVE);
}

void MMA7660::setMode(uint8_t mode)
{
    write(MMA7660_MODE,mode);
}
void MMA7660::setSampleRate(uint8_t rate)
{
    write(MMA7660_SR,rate);
}
/*Function: Get the contents of the registers in the MMA7660*/
/*          so as to calculate the acceleration.            */
unsigned char MMA7660::getXYZ(int8_t *x,int8_t *y,int8_t *z)
{

    unsigned char val[3];
    int count = 0;
    val[0] = val[1] = val[2] = 64;
    
    long timer1 = millis();
    long timer2 = 0;
    
    while(Wire.available() > 0)
    {
        timer2 = millis();
        if((timer2-timer1)>500)
        {
            return 0;
        }
    }

    Wire.read();
    Wire.requestFrom(MMA7660_ADDR,3);

    timer1 = millis();
    while(Wire.available())
    {
    
        if(count < 3)
        {

            timer1 = millis();
            while ( val[count] > 63 )  // reload the damn thing it is bad
            {
                val[count] = Wire.read();

                timer2 = millis();
                if((timer2-timer1)>50)
                {
                    return 0;
                }

            }
        }

        count++;
        
        timer2 = millis();
        
        if((timer2-timer1)>500)
        {
            return 0;
        }

    }
    
    *x = ((char)(val[0]<<2))/4;
    *y = ((char)(val[1]<<2))/4;
    *z = ((char)(val[2]<<2))/4;
    
    return 1;
}

unsigned char MMA7660::getAcceleration(float *ax,float *ay,float *az)
{
    int8_t x,y,z;
    
    if(!getXYZ(&x, &y, &z))return 0;
    *ax = x/21.00;
    *ay = y/21.00;
    *az = z/21.00;
    
    return 1;
    
}


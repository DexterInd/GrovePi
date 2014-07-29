/*****************************************************************************/
//	Function:    Header file for class MMC7660 
//  Hardware:    Grove - 3-Axis Digital Accelerometer(±1.5g)
//	Arduino IDE: Arduino-1.0
//	Author:	 Frankie.Chu		
//	Date: 	 Jan 10,2013
//	Version: v0.9b
//	by www.seeedstudio.com
//
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
#ifndef __MMC7660_H__
#define __MMC7660_H__

#define MMA7660_ADDR  0x4c

#define MMA7660_X     0x00
#define MMA7660_Y     0x01
#define MMA7660_Z     0x02
#define MMA7660_TILT  0x03
#define MMA7660_SRST  0x04
#define MMA7660_SPCNT 0x05
#define MMA7660_INTSU 0x06
#define MMA7660_MODE  0x07
	#define MMA7660_STAND_BY 0x00
	#define MMA7660_ACTIVE	 0x01	
#define MMA7660_SR    0x08		//sample rate register
	#define AUTO_SLEEP_120	0X00//120 sample per second
	#define AUTO_SLEEP_64	0X01
	#define AUTO_SLEEP_32	0X02
	#define AUTO_SLEEP_16	0X03
	#define AUTO_SLEEP_8	0X04
	#define AUTO_SLEEP_4	0X05
	#define AUTO_SLEEP_2	0X06
	#define AUTO_SLEEP_1	0X07
#define MMA7660_PDET  0x09
#define MMA7660_PD    0x0A
class MMA7660
{
private:
	void write(uint8_t _register, uint8_t _data);
	uint8_t read(uint8_t _register);
public:
	void init();
	void setMode(uint8_t mode);
	void setSampleRate(uint8_t rate);
	unsigned char getXYZ(int8_t *x,int8_t *y,int8_t *z);
	unsigned char getAcceleration(float *ax,float *ay,float *az);
};

#endif



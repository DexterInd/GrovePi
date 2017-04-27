/*
 * TH02_dev.h
 * Driver for DIGITAL I2C HUMIDITY AND TEMPERATURE SENSOR
 *
 * Copyright (c) 2014 seeed technology inc.
 * Website    : www.seeed.cc
 * Author     : Oliver Wang
 * Create Time: April 2014
 * Change Log :
 *
 * The MIT License (MIT)
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
 
#ifndef _TH02_DEV_H
#define _TH02_DEV_H

/****************************************************************************/
/***        Including Files                                               ***/
/****************************************************************************/
#include <Wire.h>
#include <Arduino.h>

/****************************************************************************/
/***        Macro Definitions                                             ***/
/****************************************************************************/
#define TH02_I2C_DEV_ID      0x40
#define REG_STATUS           0x00
#define REG_DATA_H           0x01
#define REG_DATA_L           0x02
#define REG_CONFIG           0x03
#define REG_ID               0x11

#define STATUS_RDY_MASK      0x01    //poll RDY,0 indicate the conversion is done

#define CMD_MEASURE_HUMI     0x01    //perform a humility measurement
#define CMD_MEASURE_TEMP     0x11    //perform a temperature measurement

#define TH02_WR_REG_MODE      0xC0
#define TH02_RD_REG_MODE      0x80
/****************************************************************************/
/***        Class Definition                                              ***/
/****************************************************************************/
class TH02_dev
{
public:
	void begin();
	uint8_t isAvailable();
	float ReadTemperature(void);
	float ReadHumidity(void);
private:
	void TH02_IIC_WriteCmd(uint8_t u8Cmd);
	uint8_t TH02_IIC_ReadReg(uint8_t u8Reg);
	void TH02_IIC_WriteReg(uint8_t u8Reg,uint8_t u8Data);
	uint16_t TH02_IIC_ReadData(void);
	uint16_t TH02_IIC_ReadData2byte(void);
};
extern TH02_dev TH02;

#endif  // _TH02_DEV_H

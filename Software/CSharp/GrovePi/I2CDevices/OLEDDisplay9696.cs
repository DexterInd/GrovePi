using System;
using Windows.Devices.I2c;
using GrovePi.Common;
using System.Diagnostics;

namespace GrovePi.I2CDevices
{
    public interface IOLEDDisplay9696
    {
        IOLEDDisplay9696 initialize();
        IOLEDDisplay9696 setNormalDisplay();
        IOLEDDisplay9696 sendCommand(byte cmd);
        IOLEDDisplay9696 sendData(byte Data);
        IOLEDDisplay9696 setGrayLevel(byte grayLevel);
        IOLEDDisplay9696 setVerticalMode();
        IOLEDDisplay9696 setHorizontalMode();

        IOLEDDisplay9696 setTextXY(byte Row, byte Column);
        IOLEDDisplay9696 clearDisplay();
        IOLEDDisplay9696 setContrastLevel(byte ContrastLevel);
        IOLEDDisplay9696 putChar(char C);
        IOLEDDisplay9696 putString(string text);
        //IOLEDDisplay9696 putNumber();
        //IOLEDDisplay9696 putFloat();
        //IOLEDDisplay9696 putFloat();
        IOLEDDisplay9696 drawBitmap(byte[] bitmaparray, int bytes);
        IOLEDDisplay9696 setHorizontalScrollProperties(bool direction, byte startRow, byte endRow, byte startColumn, byte endColumn, byte scrollSpeed);
        IOLEDDisplay9696 activateScroll();
        IOLEDDisplay9696 deactivateScroll();

    }
    internal sealed class OLEDDisplay9696 : IOLEDDisplay9696
    {
        private const byte VERTICAL_MODE = 1;
        private const byte HORIZONTAL_MODE = 2;

        private const byte SeeedGrayOLED_Address = 0x3c;
        private const byte SeeedGrayOLED_Command_Mode = 0x80;
        private const byte SeeedGrayOLED_Data_Mode = 0x40;

        private const byte SeeedGrayOLED_Display_Off_Cmd = 0xAE;
        private const byte SeeedGrayOLED_Display_On_Cmd = 0xAF;

        private const byte SeeedGrayOLED_Normal_Display_Cmd = 0xA4;
        private const byte SeeedGrayOLED_Inverse_Display_Cmd = 0xA7;
        private const byte SeeedGrayOLED_Activate_Scroll_Cmd = 0x2F;
        private const byte SeeedGrayOLED_Dectivate_Scroll_Cmd = 0x2E;
        private const byte SeeedGrayOLED_Set_ContrastLevel_Cmd = 0x81;

        private const byte Scroll_Left = 0x00;
        private const byte Scroll_Right = 0x01;

        private const byte Scroll_2Frames = 0x7;
        private const byte Scroll_3Frames = 0x4;
        private const byte Scroll_4Frames = 0x5;
        private const byte Scroll_5Frames = 0x0;
        private const byte Scroll_25Frames = 0x6;
        private const byte Scroll_64Frames = 0x1;
        private const byte Scroll_128Frames = 0x2;
        private const byte Scroll_256Frames = 0x3;

        private byte grayH = 0;
        private byte grayL = 0;
        private byte addressingMode = 0;

        private byte[,] BasicFont = new byte[,]
        {
            {0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
            {0x00,0x00,0x5F,0x00,0x00,0x00,0x00,0x00},
            {0x00,0x00,0x07,0x00,0x07,0x00,0x00,0x00},
            {0x00,0x14,0x7F,0x14,0x7F,0x14,0x00,0x00},
            {0x00,0x24,0x2A,0x7F,0x2A,0x12,0x00,0x00},
            {0x00,0x23,0x13,0x08,0x64,0x62,0x00,0x00},
            {0x00,0x36,0x49,0x55,0x22,0x50,0x00,0x00},
            {0x00,0x00,0x05,0x03,0x00,0x00,0x00,0x00},
            {0x00,0x1C,0x22,0x41,0x00,0x00,0x00,0x00},
            {0x00,0x41,0x22,0x1C,0x00,0x00,0x00,0x00},
            {0x00,0x08,0x2A,0x1C,0x2A,0x08,0x00,0x00},
            {0x00,0x08,0x08,0x3E,0x08,0x08,0x00,0x00},
            {0x00,0xA0,0x60,0x00,0x00,0x00,0x00,0x00},
            {0x00,0x08,0x08,0x08,0x08,0x08,0x00,0x00},
            {0x00,0x60,0x60,0x00,0x00,0x00,0x00,0x00},
            {0x00,0x20,0x10,0x08,0x04,0x02,0x00,0x00},
            {0x00,0x3E,0x51,0x49,0x45,0x3E,0x00,0x00},
            {0x00,0x00,0x42,0x7F,0x40,0x00,0x00,0x00},
            {0x00,0x62,0x51,0x49,0x49,0x46,0x00,0x00},
            {0x00,0x22,0x41,0x49,0x49,0x36,0x00,0x00},
            {0x00,0x18,0x14,0x12,0x7F,0x10,0x00,0x00},
            {0x00,0x27,0x45,0x45,0x45,0x39,0x00,0x00},
            {0x00,0x3C,0x4A,0x49,0x49,0x30,0x00,0x00},
            {0x00,0x01,0x71,0x09,0x05,0x03,0x00,0x00},
            {0x00,0x36,0x49,0x49,0x49,0x36,0x00,0x00},
            {0x00,0x06,0x49,0x49,0x29,0x1E,0x00,0x00},
            {0x00,0x00,0x36,0x36,0x00,0x00,0x00,0x00},
            {0x00,0x00,0xAC,0x6C,0x00,0x00,0x00,0x00},
            {0x00,0x08,0x14,0x22,0x41,0x00,0x00,0x00},
            {0x00,0x14,0x14,0x14,0x14,0x14,0x00,0x00},
            {0x00,0x41,0x22,0x14,0x08,0x00,0x00,0x00},
            {0x00,0x02,0x01,0x51,0x09,0x06,0x00,0x00},
            {0x00,0x32,0x49,0x79,0x41,0x3E,0x00,0x00},
            {0x00,0x7E,0x09,0x09,0x09,0x7E,0x00,0x00},
            {0x00,0x7F,0x49,0x49,0x49,0x36,0x00,0x00},
            {0x00,0x3E,0x41,0x41,0x41,0x22,0x00,0x00},
            {0x00,0x7F,0x41,0x41,0x22,0x1C,0x00,0x00},
            {0x00,0x7F,0x49,0x49,0x49,0x41,0x00,0x00},
            {0x00,0x7F,0x09,0x09,0x09,0x01,0x00,0x00},
            {0x00,0x3E,0x41,0x41,0x51,0x72,0x00,0x00},
            {0x00,0x7F,0x08,0x08,0x08,0x7F,0x00,0x00},
            {0x00,0x41,0x7F,0x41,0x00,0x00,0x00,0x00},
            {0x00,0x20,0x40,0x41,0x3F,0x01,0x00,0x00},
            {0x00,0x7F,0x08,0x14,0x22,0x41,0x00,0x00},
            {0x00,0x7F,0x40,0x40,0x40,0x40,0x00,0x00},
            {0x00,0x7F,0x02,0x0C,0x02,0x7F,0x00,0x00},
            {0x00,0x7F,0x04,0x08,0x10,0x7F,0x00,0x00},
            {0x00,0x3E,0x41,0x41,0x41,0x3E,0x00,0x00},
            {0x00,0x7F,0x09,0x09,0x09,0x06,0x00,0x00},
            {0x00,0x3E,0x41,0x51,0x21,0x5E,0x00,0x00},
            {0x00,0x7F,0x09,0x19,0x29,0x46,0x00,0x00},
            {0x00,0x26,0x49,0x49,0x49,0x32,0x00,0x00},
            {0x00,0x01,0x01,0x7F,0x01,0x01,0x00,0x00},
            {0x00,0x3F,0x40,0x40,0x40,0x3F,0x00,0x00},
            {0x00,0x1F,0x20,0x40,0x20,0x1F,0x00,0x00},
            {0x00,0x3F,0x40,0x38,0x40,0x3F,0x00,0x00},
            {0x00,0x63,0x14,0x08,0x14,0x63,0x00,0x00},
            {0x00,0x03,0x04,0x78,0x04,0x03,0x00,0x00},
            {0x00,0x61,0x51,0x49,0x45,0x43,0x00,0x00},
            {0x00,0x7F,0x41,0x41,0x00,0x00,0x00,0x00},
            {0x00,0x02,0x04,0x08,0x10,0x20,0x00,0x00},
            {0x00,0x41,0x41,0x7F,0x00,0x00,0x00,0x00},
            {0x00,0x04,0x02,0x01,0x02,0x04,0x00,0x00},
            {0x00,0x80,0x80,0x80,0x80,0x80,0x00,0x00},
            {0x00,0x01,0x02,0x04,0x00,0x00,0x00,0x00},
            {0x00,0x20,0x54,0x54,0x54,0x78,0x00,0x00},
            {0x00,0x7F,0x48,0x44,0x44,0x38,0x00,0x00},
            {0x00,0x38,0x44,0x44,0x28,0x00,0x00,0x00},
            {0x00,0x38,0x44,0x44,0x48,0x7F,0x00,0x00},
            {0x00,0x38,0x54,0x54,0x54,0x18,0x00,0x00},
            {0x00,0x08,0x7E,0x09,0x02,0x00,0x00,0x00},
            {0x00,0x18,0xA4,0xA4,0xA4,0x7C,0x00,0x00},
            {0x00,0x7F,0x08,0x04,0x04,0x78,0x00,0x00},
            {0x00,0x00,0x7D,0x00,0x00,0x00,0x00,0x00},
            {0x00,0x80,0x84,0x7D,0x00,0x00,0x00,0x00},
            {0x00,0x7F,0x10,0x28,0x44,0x00,0x00,0x00},
            {0x00,0x41,0x7F,0x40,0x00,0x00,0x00,0x00},
            {0x00,0x7C,0x04,0x18,0x04,0x78,0x00,0x00},
            {0x00,0x7C,0x08,0x04,0x7C,0x00,0x00,0x00},
            {0x00,0x38,0x44,0x44,0x38,0x00,0x00,0x00},
            {0x00,0xFC,0x24,0x24,0x18,0x00,0x00,0x00},
            {0x00,0x18,0x24,0x24,0xFC,0x00,0x00,0x00},
            {0x00,0x00,0x7C,0x08,0x04,0x00,0x00,0x00},
            {0x00,0x48,0x54,0x54,0x24,0x00,0x00,0x00},
            {0x00,0x04,0x7F,0x44,0x00,0x00,0x00,0x00},
            {0x00,0x3C,0x40,0x40,0x7C,0x00,0x00,0x00},
            {0x00,0x1C,0x20,0x40,0x20,0x1C,0x00,0x00},
            {0x00,0x3C,0x40,0x30,0x40,0x3C,0x00,0x00},
            {0x00,0x44,0x28,0x10,0x28,0x44,0x00,0x00},
            {0x00,0x1C,0xA0,0xA0,0x7C,0x00,0x00,0x00},
            {0x00,0x44,0x64,0x54,0x4C,0x44,0x00,0x00},
            {0x00,0x08,0x36,0x41,0x00,0x00,0x00,0x00},
            {0x00,0x00,0x7F,0x00,0x00,0x00,0x00,0x00},
            {0x00,0x41,0x36,0x08,0x00,0x00,0x00,0x00},
            {0x00,0x02,0x01,0x01,0x02,0x01,0x00,0x00},
            {0x00,0x02,0x05,0x05,0x02,0x00,0x00,0x00}
        };

        internal OLEDDisplay9696(I2cDevice Device)
        {
            if (Device == null) throw new ArgumentNullException(nameof(Device));

            DirectAccess = Device;
        }

        public IOLEDDisplay9696 initialize()
        {
            this.sendCommand(0xFD);  // unlock IC MCU from entering command.
            this.sendCommand(0x12);
            this.sendCommand(0xAE); // Set display off
            this.sendCommand(0xA8); // set multiplex ratio
            this.sendCommand(0x5F); // 96
            this.sendCommand(0xA1); // set display start line
            this.sendCommand(0x00);
            this.sendCommand(0xA2); // set display offset
            this.sendCommand(0x60);
            this.sendCommand(0xA0); // set remap
            this.sendCommand(0x46);
            this.sendCommand(0xAB); // set vdd internal
            this.sendCommand(0x01); //
            this.sendCommand(0x81); // set contrasr
            this.sendCommand(0x53); // 100 nit
            this.sendCommand(0xB1); // Set Phase Length
            this.sendCommand(0X51); //
            this.sendCommand(0xB3); // Set Display Clock Divide Ratio/Oscillator Frequency
            this.sendCommand(0x01);
            this.sendCommand(0xB9); //
            this.sendCommand(0xBC); // set pre_charge voltage/VCOMH
            this.sendCommand(0x08); // (0x08);
            this.sendCommand(0xBE); // set VCOMH
            this.sendCommand(0X07); // (0x07);
            this.sendCommand(0xB6); // Set second pre-charge period
            this.sendCommand(0x01); //
            this.sendCommand(0xD5); // enable second precharge and enternal vsl
            this.sendCommand(0X62); // (0x62);
            this.sendCommand(0xA4); // Set Normal Display Mode
            this.sendCommand(0x2E); // Deactivate Scroll
            this.sendCommand(0xAF); // Switch on display
            Delay.Milliseconds(100);

            // Row Address
            this.sendCommand(0x75);    // Set Row Address 
            this.sendCommand(0x00);    // Start 0
            this.sendCommand(0x5f);    // End 95 


            // Column Address
            this.sendCommand(0x15);    // Set Column Address 
            this.sendCommand(0x08);    // Start from 8th Column of driver IC. This is 0th Column for OLED 
            this.sendCommand(0x37);    // End at  (8 + 47)th column. Each Column has 2 pixels(segments)

            // Init gray level for text. Default:Brightest White
            grayH = 0xF0;
            grayL = 0x0F;

            return this;
        }

        internal I2cDevice DirectAccess { get; }

        public IOLEDDisplay9696 sendCommand(byte cmd)
        {
            DirectAccess.Write(new byte[] { SeeedGrayOLED_Command_Mode, cmd });
            return this;
        }

        public IOLEDDisplay9696 setContrastLevel(byte ContrastLevel)
        {
            this.sendCommand(SeeedGrayOLED_Set_ContrastLevel_Cmd);
            this.sendCommand(ContrastLevel);
            return this;
        }

        public IOLEDDisplay9696 setHorizontalMode()
        {
            this.sendCommand(0xA0); // remap to
            this.sendCommand(0x42); // horizontal mode

            // Row Address
            this.sendCommand(0x75);    // Set Row Address 
            this.sendCommand(0x00);    // Start 0
            this.sendCommand(0x5f);    // End 95 

            // Column Address
            this.sendCommand(0x15);    // Set Column Address 
            this.sendCommand(0x08);    // Start from 8th Column of driver IC. This is 0th Column for OLED 
            this.sendCommand(0x37);    // End at  (8 + 47)th column. Each Column has 2 pixels(or segments)

            return this;
        }


        public IOLEDDisplay9696 setVerticalMode()
        {
            this.sendCommand(0xA0); // remap to
            this.sendCommand(0x46); // Vertical mode

            return this;
        }

        public IOLEDDisplay9696 setTextXY(byte Row, byte Column)
        {
            //Column Address
            this.sendCommand(0x15);             /* Set Column Address */
            this.sendCommand((byte)(0x08 + (Column * 4)));  /* Start Column: Start from 8 */
            this.sendCommand(0x37);             /* End Column */
            // Row Address
            this.sendCommand(0x75);             /* Set Row Address */
            this.sendCommand((byte)(0x00 + (Row * 8)));     /* Start Row*/
            this.sendCommand((byte)(0x07 + (Row * 8)));     /* End Row*/

            return this;
        }
        public IOLEDDisplay9696 clearDisplay()
        {
            byte i, j;
            for (j = 0; j < 48; j++)
            {
                for (i = 0; i < 96; i++)  //clear all columns
                {
                    this.sendData(0x00);
                }
            }

            return this;

        }

        public IOLEDDisplay9696 sendData(byte Data)
        {
            DirectAccess.Write(new byte[] { SeeedGrayOLED_Data_Mode, Data });
            return this;
        }

        public IOLEDDisplay9696 setGrayLevel(byte grayLevel)
        {
            grayH = (byte)((grayLevel << 4) & 0xF0);
            grayL = (byte)(grayLevel & 0x0F);

            return this;
        }

        public IOLEDDisplay9696 putChar(char C)
        {
            if (C < 32 || C > 127) //Ignore non-printable ASCII characters. This can be modified for multilingual font.
            {
                C = ' '; //Space
            }


            for (int i = 0; i < 8; i = i + 2)
            {
                for (int j = 0; j < 8; j++)
                {
                    // Character is constructed two pixel at a time using vertical mode from the default 8x8 font
                    byte c = 0x00;
                    byte bit1 = (byte)((BasicFont[C - 32, i] >> j) & 0x01);
                    byte bit2 = (byte)((BasicFont[C - 32, i + 1] >> j) & 0x01);
                    // Each bit is changed to a nibble
                    c |= (byte)((bit1.Equals(0x01)) ? grayH : 0x00);
                    c |= (byte)((bit2.Equals(0x01)) ? grayL : 0x00);
                    this.sendData(c);
                }
            }

            return this;
        }

        public IOLEDDisplay9696 putString(string text)
        {
            foreach (var C in text)
            {
                this.putChar(C);
            }

            return this;
        }

        public IOLEDDisplay9696 drawBitmap(byte[] bitmaparray, int bytes)
        {
            byte localAddressMode = this.addressingMode;
            if (addressingMode != HORIZONTAL_MODE)
            {
                //Bitmap is drawn in horizontal mode
                this.setHorizontalMode();
            }

            //for (int i = 0; i < bytes; i++)
            foreach (var Byte in bitmaparray)
            {
                for (int j = 0; j < 8; j = j + 2)
                {
                    byte c = 0x00;
                    byte bit1 = (byte)(Byte << j & 0x80);
                    byte bit2 = (byte)(Byte << (j + 1) & 0x80);

                    // Each bit is changed to a nibble
                    c |= (byte)((bit1.Equals(0x80)) ? grayH : 0x00);
                    // Each bit is changed to a nibble
                    c |= (byte)((bit2.Equals(0x80)) ? grayL : 0x00);
                    this.sendData(c);
                }
            }
            if (localAddressMode == VERTICAL_MODE)
            {
                //If Vertical Mode was used earlier, restore it.
                this.setVerticalMode();
            }

            return this;

        }

        public IOLEDDisplay9696 setHorizontalScrollProperties(bool direction, byte startRow, byte endRow, byte startColumn, byte endColumn, byte scrollSpeed)
        {
            /*
        Use the following defines for 'direction' :

         Scroll_Left            
         Scroll_Right           

        Use the following defines for 'scrollSpeed' :

         Scroll_2Frames     
         Scroll_3Frames
         Scroll_4Frames
         Scroll_5Frames 
         Scroll_25Frames
         Scroll_64Frames
         Scroll_128Frames
         Scroll_256Frames

        */

            if (Scroll_Right.Equals(direction))
            {
                //Scroll Right
                this.sendCommand(0x27);
            }
            else
            {
                //Scroll Left  
                this.sendCommand(0x26);
            }
            this.sendCommand(0x00);       //Dummmy byte
            this.sendCommand(startRow);
            this.sendCommand(scrollSpeed);
            this.sendCommand(endRow);
            this.sendCommand((byte)(startColumn + 8));
            this.sendCommand((byte)(endColumn + 8));
            this.sendCommand(0x00);      //Dummmy byte

            return this;

        }

        public IOLEDDisplay9696 activateScroll()
        {
            this.sendCommand(SeeedGrayOLED_Activate_Scroll_Cmd);
            return this;
        }

        public IOLEDDisplay9696 deactivateScroll()
        {
            this.sendCommand(SeeedGrayOLED_Dectivate_Scroll_Cmd);
            return this;
        }

        public IOLEDDisplay9696 setNormalDisplay()
        {
            this.sendCommand(SeeedGrayOLED_Normal_Display_Cmd);
            return this;
        }

        public IOLEDDisplay9696 setInverseDisplay()
        {
            this.sendCommand(SeeedGrayOLED_Inverse_Display_Cmd);
            return this;
        }


    }
}

using System;
using GrovePi.I2CDevices.Configuration;
using Windows.Devices.I2c;

namespace GrovePi.I2CDevices
{

    public interface IThreeAxisAccelerometerADXL345
    {
        IThreeAxisAccelerometerADXL345 powerOn();
        // IThreeAxisAccelerometerADXL345 readAccel(int* xyx);
        // IThreeAxisAccelerometerADXL345 readXYZ(int* x, int* y, int* z);
        // IThreeAxisAccelerometerADXL345 getAcceleration(double* xyz);

        // IThreeAxisAccelerometerADXL345 setTapThreshold(int tapThreshold);
        // IThreeAxisAccelerometerADXL345 getTapThreshold();
        // IThreeAxisAccelerometerADXL345 setAxisGains(double* _gains);
        // IThreeAxisAccelerometerADXL345 getAxisGains(double* _gains);
        // IThreeAxisAccelerometerADXL345 setAxisOffset(int x, int y, int z);
        // IThreeAxisAccelerometerADXL345 getAxisOffset(int* x, int* y, int* z);
        // IThreeAxisAccelerometerADXL345 setTapDuration(int tapDuration);
        // IThreeAxisAccelerometerADXL345 getTapDuration();
        // IThreeAxisAccelerometerADXL345 setDoubleTapLatency(int doubleTapLatency);
        // IThreeAxisAccelerometerADXL345 getDoubleTapLatency();
        // IThreeAxisAccelerometerADXL345 setDoubleTapWindow(int doubleTapWindow);
        // IThreeAxisAccelerometerADXL345 getDoubleTapWindow();
        // IThreeAxisAccelerometerADXL345 setActivityThreshold(int activityThreshold);
        // IThreeAxisAccelerometerADXL345 getActivityThreshold();
        // IThreeAxisAccelerometerADXL345 setInactivityThreshold(int inactivityThreshold);
        // IThreeAxisAccelerometerADXL345 getInactivityThreshold();
        // IThreeAxisAccelerometerADXL345 setTimeInactivity(int timeInactivity);
        // IThreeAxisAccelerometerADXL345 getTimeInactivity();
        // IThreeAxisAccelerometerADXL345 setFreeFallThreshold(int freeFallthreshold);
        // IThreeAxisAccelerometerADXL345 getFreeFallThreshold();
        // IThreeAxisAccelerometerADXL345 setFreeFallDuration(int freeFallDuration);
        // IThreeAxisAccelerometerADXL345 getFreeFallDuration();

        // IThreeAxisAccelerometerADXL345 isActivityXEnabled();
        // IThreeAxisAccelerometerADXL345 isActivityYEnabled();
        // IThreeAxisAccelerometerADXL345 isActivityZEnabled();
        // IThreeAxisAccelerometerADXL345 isInactivityXEnabled();
        // IThreeAxisAccelerometerADXL345 isInactivityYEnabled();
        // IThreeAxisAccelerometerADXL345 isInactivityZEnabled();
        // IThreeAxisAccelerometerADXL345 isActivityAc();
        // IThreeAxisAccelerometerADXL345 isInactivityAc();
        // IThreeAxisAccelerometerADXL345 setActivityAc(bool state);
        // IThreeAxisAccelerometerADXL345 setInactivityAc(bool state);

        // IThreeAxisAccelerometerADXL345 getSuppressBit();
        // IThreeAxisAccelerometerADXL345 setSuppressBit(bool state);
        // IThreeAxisAccelerometerADXL345 isTapDetectionOnX();
        // IThreeAxisAccelerometerADXL345 setTapDetectionOnX(bool state);
        // IThreeAxisAccelerometerADXL345 isTapDetectionOnY();
        // IThreeAxisAccelerometerADXL345 setTapDetectionOnY(bool state);
        // IThreeAxisAccelerometerADXL345 isTapDetectionOnZ();
        // IThreeAxisAccelerometerADXL345 setTapDetectionOnZ(bool state);

        // IThreeAxisAccelerometerADXL345 setActivityX(bool state);
        // IThreeAxisAccelerometerADXL345 setActivityY(bool state);
        // IThreeAxisAccelerometerADXL345 setActivityZ(bool state);
        // IThreeAxisAccelerometerADXL345 setInactivityX(bool state);
        // IThreeAxisAccelerometerADXL345 setInactivityY(bool state);
        // IThreeAxisAccelerometerADXL345 setInactivityZ(bool state);

        // IThreeAxisAccelerometerADXL345 isActivitySourceOnX();
        // IThreeAxisAccelerometerADXL345 isActivitySourceOnY();
        // IThreeAxisAccelerometerADXL345 isActivitySourceOnZ();
        // IThreeAxisAccelerometerADXL345 isTapSourceOnX();
        // IThreeAxisAccelerometerADXL345 isTapSourceOnY();
        // IThreeAxisAccelerometerADXL345 isTapSourceOnZ();
        // IThreeAxisAccelerometerADXL345 isAsleep();

        // IThreeAxisAccelerometerADXL345 isLowPower();
        // IThreeAxisAccelerometerADXL345 setLowPower(bool state);
        // IThreeAxisAccelerometerADXL345 getRate();
        // IThreeAxisAccelerometerADXL345 setRate(double rate);
        // IThreeAxisAccelerometerADXL345 set_bw(byte bw_code);
        // IThreeAxisAccelerometerADXL345 get_bw_code();


        // IThreeAxisAccelerometerADXL345 triggered(byte interrupts, int mask);


        // IThreeAxisAccelerometerADXL345 getInterruptSource();
        // IThreeAxisAccelerometerADXL345 getInterruptSource(byte interruptBit);
        // IThreeAxisAccelerometerADXL345 getInterruptMapping(byte interruptBit);
        // IThreeAxisAccelerometerADXL345 setInterruptMapping(byte interruptBit, bool interruptPin);
        // IThreeAxisAccelerometerADXL345 isInterruptEnabled(byte interruptBit);
        // IThreeAxisAccelerometerADXL345 setInterrupt(byte interruptBit, bool state);

        // IThreeAxisAccelerometerADXL345 getRangeSetting(byte* rangeSetting);
        // IThreeAxisAccelerometerADXL345 setRangeSetting(int val);
        // IThreeAxisAccelerometerADXL345 getSelfTestBit();
        // IThreeAxisAccelerometerADXL345 setSelfTestBit(bool selfTestBit);
        // IThreeAxisAccelerometerADXL345 getSpiBit();
        // IThreeAxisAccelerometerADXL345 setSpiBit(bool spiBit);
        // IThreeAxisAccelerometerADXL345 getInterruptLevelBit();
        // IThreeAxisAccelerometerADXL345 setInterruptLevelBit(bool interruptLevelBit);
        // IThreeAxisAccelerometerADXL345 getFullResBit();
        // IThreeAxisAccelerometerADXL345 setFullResBit(bool fullResBit);
        // IThreeAxisAccelerometerADXL345 getJustifyBit();
        // IThreeAxisAccelerometerADXL345 setJustifyBit(bool justifyBit);
        // IThreeAxisAccelerometerADXL345 printAllRegister();

        IThreeAxisAccelerometerADXL345 writeTo(byte address, byte val);
        // IThreeAxisAccelerometerADXL345 readFrom(byte address, int num, byte buff[]);
        // IThreeAxisAccelerometerADXL345 setRegisterBit(byte regAdress, int bitPos, bool state);
        // IThreeAxisAccelerometerADXL345 getRegisterBit(byte regAdress, int bitPos);
        // IThreeAxisAccelerometerADXL345 _buff[6];    //6 bytes buffer for saving data read from the device
    }

    internal sealed class ThreeAxisAccelerometerADXL345 : IThreeAxisAccelerometerADXL345
    {

        /* ------- Register names ------- */
        private const byte ADXL345_DEVID = 0x00;
        private const byte ADXL345_RESERVED1 = 0x01;
        private const byte ADXL345_THRESH_TAP = 0x1d;
        private const byte ADXL345_OFSX = 0x1e;
        private const byte ADXL345_OFSY = 0x1f;
        private const byte ADXL345_OFSZ = 0x20;
        private const byte ADXL345_DUR = 0x21;
        private const byte ADXL345_LATENT = 0x22;
        private const byte ADXL345_WINDOW = 0x23;
        private const byte ADXL345_THRESH_ACT = 0x24;
        private const byte ADXL345_THRESH_INACT = 0x25;
        private const byte ADXL345_TIME_INACT = 0x26;
        private const byte ADXL345_ACT_INACT_CTL = 0x27;
        private const byte ADXL345_THRESH_FF = 0x28;
        private const byte ADXL345_TIME_FF = 0x29;
        private const byte ADXL345_TAP_AXES = 0x2a;
        private const byte ADXL345_ACT_TAP_STATUS = 0x2b;
        private const byte ADXL345_BW_RATE = 0x2c;
        private const byte ADXL345_POWER_CTL = 0x2d;
        private const byte ADXL345_INT_ENABLE = 0x2e;
        private const byte ADXL345_INT_MAP = 0x2f;
        private const byte ADXL345_INT_SOURCE = 0x30;
        private const byte ADXL345_DATA_FORMAT = 0x31;
        private const byte ADXL345_DATAX0 = 0x32;
        private const byte ADXL345_DATAX1 = 0x33;
        private const byte ADXL345_DATAY0 = 0x34;
        private const byte ADXL345_DATAY1 = 0x35;
        private const byte ADXL345_DATAZ0 = 0x36;
        private const byte ADXL345_DATAZ1 = 0x37;
        private const byte ADXL345_FIFO_CTL = 0x38;
        private const byte ADXL345_FIFO_STATUS = 0x39;

        private const byte ADXL345_BW_1600 = 0xF;
        private const byte ADXL345_BW_800  = 0xE;
        private const byte ADXL345_BW_400  = 0xD;
        private const byte ADXL345_BW_200  = 0xC;
        private const byte ADXL345_BW_100  = 0xB;
        private const byte ADXL345_BW_50   = 0xA;
        private const byte ADXL345_BW_25   = 0x9;
        private const byte ADXL345_BW_12   = 0x8;
        private const byte ADXL345_BW_6    = 0x7;
        private const byte ADXL345_BW_3    = 0x6;

        /* 
         Interrupt PINs
         INT1: 0
         INT2: 1
         */
        private const byte ADXL345_INT1_PIN = 0x00;
        private const byte ADXL345_INT2_PIN = 0x01;

        /*Interrupt bit position*/
        private const byte ADXL345_INT_DATA_READY_BIT = 0x07;
        private const byte ADXL345_INT_SINGLE_TAP_BIT = 0x06;
        private const byte ADXL345_INT_DOUBLE_TAP_BIT = 0x05;
        private const byte ADXL345_INT_ACTIVITY_BIT   = 0x04;
        private const byte ADXL345_INT_INACTIVITY_BIT = 0x03;
        private const byte ADXL345_INT_FREE_FALL_BIT  = 0x02;
        private const byte ADXL345_INT_WATERMARK_BIT  = 0x01;
        private const byte ADXL345_INT_OVERRUNY_BIT   = 0x00;

        private const byte ADXL345_DATA_READY = 0x07;
        private const byte ADXL345_SINGLE_TAP = 0x06;
        private const byte ADXL345_DOUBLE_TAP = 0x05;
        private const byte ADXL345_ACTIVITY   = 0x04;
        private const byte ADXL345_INACTIVITY = 0x03;
        private const byte ADXL345_FREE_FALL  = 0x02;
        private const byte ADXL345_WATERMARK  = 0x01;
        private const byte ADXL345_OVERRUNY   = 0x00;

        private const bool ADXL345_OK    = 1; // no error
        private const bool ADXL345_ERROR = false; // indicates error is predent

        private const byte ADXL345_NO_ERROR   = 0; // initial state
        private const byte ADXL345_READ_ERROR = 1; // problem reading accel
        private const byte ADXL345_BAD_ARG    = 2; // bad method argument

        public byte ADXL345_TO_READ = 6;
        public byte ADXL345_DEVICE = 0x53;

        public bool status;           // set when error occurs 
        // see error code for details
        public byte error_code;       // Initial state
        public double[] gains = new double[3];        // counts to Gs
        // public double[] xyz;
        public byte[] _buff = new byte[6];

        internal I2cDevice DirectAccess{ get; }
        internal ThreeAxisAccelerometerADXL345(I2cDevice device)
        {
            if (device == null) throw new ArgumentNullException(nameof(device));
            DirectAccess = device;
        }

        public IThreeAxisAccelerometerADXL345 powerOn()
        {
            //Turning on the ADXL345
            writeTo(ADXL345_POWER_CTL, 0);
            writeTo(ADXL345_POWER_CTL, 16);
            writeTo(ADXL345_POWER_CTL, 8);

            return this;
        }

        // Reads the acceleration into three variable x, y and z
        public int[] readAccel()
        {
            return readXYZ();
        }

         private int[] readXYZ()
         {
            int[] xyz = new int[3];

             readFrom(ADXL345_DATAX0, ADXL345_TO_READ, _buff); //read the acceleration data from the ADXL345
             xyz[0] = (Int16)(((UInt16)_buff[1] << 8) | _buff[0]);   
             xyz[1] = (Int16)(((UInt16)_buff[3] << 8) | _buff[2]);
             xyz[2] = (Int16)(((UInt16)_buff[5] << 8) | _buff[4]);

            return xyz;
         }

        // public void getAcceleration(double *xyz)
        // {
        //     int i;
        //     int xyz_int[3];
        //     readAccel(xyz_int);
        //     for(i=0; i<3; i++){
        //         xyz[i] = xyz_int[i] * gains[i];
        //     }
        // }
        // Writes val to address register on device
        public IThreeAxisAccelerometerADXL345 writeTo(byte address, byte val)
        {
            DirectAccess.Write(new[] { address, val });
            return this;
        }

        // Reads num bytes starting from address register on device in to _buff array
        public void readFrom(byte address, int num, byte[] _buff)
        {

            DirectAccess.WriteRead(new byte[] { ADXL345_DEVICE, address }, _buff);
            if(_buff.Length != num)
            {
                status = ADXL345_ERROR;
                error_code = ADXL345_READ_ERROR;
            }
        }

        // // Gets the range setting and return it into rangeSetting
        // // it can be 2, 4, 8 or 16
        // public void getRangeSetting(byte* rangeSetting) 
        // {
        //     byte _b;
        //     readFrom(ADXL345_DATA_FORMAT, 1, &_b);
        //     *rangeSetting = _b & B00000011;
        // }

        // // Sets the range setting, possible values are: 2, 4, 8, 16
        // public void setRangeSetting(int val) {
        //     byte _s;
        //     byte _b;

        //     switch (val) {
        //         case 2:  
        //             _s = B00000000; 
        //             break;
        //         case 4:  
        //             _s = B00000001; 
        //             break;
        //         case 8:  
        //             _s = B00000010; 
        //             break;
        //         case 16: 
        //             _s = B00000011; 
        //             break;
        //         default: 
        //             _s = B00000000;
        //     }
        //     readFrom(ADXL345_DATA_FORMAT, 1, &_b);
        //     _s |= (_b & B11101100);
        //     writeTo(ADXL345_DATA_FORMAT, _s);
        // }
        // // gets the state of the SELF_TEST bit
        // public bool getSelfTestBit() {
        //     return getRegisterBit(ADXL345_DATA_FORMAT, 7);
        // }

        // // Sets the SELF-TEST bit
        // // if set to 1 it applies a self-test force to the sensor causing a shift in the output data
        // // if set to 0 it disables the self-test force
        // public void setSelfTestBit(bool selfTestBit) {
        //     setRegisterBit(ADXL345_DATA_FORMAT, 7, selfTestBit);
        // }

        // // Gets the state of the SPI bit
        // public bool getSpiBit() {
        //     return getRegisterBit(ADXL345_DATA_FORMAT, 6);
        // }

        // // Sets the SPI bit
        // // if set to 1 it sets the device to 3-wire mode
        // // if set to 0 it sets the device to 4-wire SPI mode
        // public void setSpiBit(bool spiBit) {
        //     setRegisterBit(ADXL345_DATA_FORMAT, 6, spiBit);
        // }

        // // Gets the state of the INT_INVERT bit
        // public bool getInterruptLevelBit() {
        //     return getRegisterBit(ADXL345_DATA_FORMAT, 5);
        // }

        // // Sets the INT_INVERT bit
        // // if set to 0 sets the interrupts to active high
        // // if set to 1 sets the interrupts to active low
        // public void setInterruptLevelBit(bool interruptLevelBit) {
        //     setRegisterBit(ADXL345_DATA_FORMAT, 5, interruptLevelBit);
        // }

        // // Gets the state of the FULL_RES bit
        // public bool getFullResBit() {
        //     return getRegisterBit(ADXL345_DATA_FORMAT, 3);
        // }

        // // Sets the FULL_RES bit
        // // if set to 1, the device is in full resolution mode, where the output resolution increases with the
        // //   g range set by the range bits to maintain a 4mg/LSB scal factor
        // // if set to 0, the device is in 10-bit mode, and the range buts determine the maximum g range
        // //   and scale factor
        // public void setFullResBit(bool fullResBit) {
        //     setRegisterBit(ADXL345_DATA_FORMAT, 3, fullResBit);
        // }

        // // Gets the state of the justify bit
        // public bool getJustifyBit() {
        //     return getRegisterBit(ADXL345_DATA_FORMAT, 2);
        // }

        // // Sets the JUSTIFY bit
        // // if sets to 1 selects the left justified mode
        // // if sets to 0 selects right justified mode with sign extension
        // public void setJustifyBit(bool justifyBit) {
        //     setRegisterBit(ADXL345_DATA_FORMAT, 2, justifyBit);
        // }

        // // Sets the THRESH_TAP byte value
        // // it should be between 0 and 255
        // // the scale factor is 62.5 mg/LSB
        // // A value of 0 may result in undesirable behavior
        // public void setTapThreshold(int tapThreshold) {
        //     tapThreshold = constrain(tapThreshold,0,255);
        //     byte _b = byte (tapThreshold);
        //     writeTo(ADXL345_THRESH_TAP, _b);  
        // }

        // // Gets the THRESH_TAP byte value
        // // return value is comprised between 0 and 255
        // // the scale factor is 62.5 mg/LSB
        // public int getTapThreshold() {
        //     byte _b;
        //     readFrom(ADXL345_THRESH_TAP, 1, &_b);  
        //     return int (_b);
        // }

        // // set/get the gain for each axis in Gs / count
        // public void setAxisGains(double *_gains){
        //     int i;
        //     for(i = 0; i < 3; i++){
        //         gains[i] = _gains[i];
        //     }
        // }
        // public void getAxisGains(double *_gains){
        //     int i;
        //     for(i = 0; i < 3; i++){
        //         _gains[i] = gains[i];
        //     }
        // }


        // // Sets the OFSX, OFSY and OFSZ bytes
        // // OFSX, OFSY and OFSZ are user offset adjustments in twos complement format with
        // // a scale factor of 15,6mg/LSB
        // // OFSX, OFSY and OFSZ should be comprised between 
        // public void setAxisOffset(int x, int y, int z) {
        //     writeTo(ADXL345_OFSX, byte (x));  
        //     writeTo(ADXL345_OFSY, byte (y));  
        //     writeTo(ADXL345_OFSZ, byte (z));  
        // }

        // // Gets the OFSX, OFSY and OFSZ bytes
        // public void getAxisOffset(int* x, int* y, int*z) {
        //     byte _b;
        //     readFrom(ADXL345_OFSX, 1, &_b);  
        //     *x = int (_b);
        //     readFrom(ADXL345_OFSY, 1, &_b);  
        //     *y = int (_b);
        //     readFrom(ADXL345_OFSZ, 1, &_b);  
        //     *z = int (_b);
        // }

        // // Sets the DUR byte
        // // The DUR byte contains an unsigned time value representing the maximum time
        // // that an event must be above THRESH_TAP threshold to qualify as a tap event
        // // The scale factor is 625µs/LSB
        // // A value of 0 disables the tap/double tap funcitons. Max value is 255.
        // public void setTapDuration(int tapDuration) {
        //     tapDuration = constrain(tapDuration,0,255);
        //     byte _b = byte (tapDuration);
        //     writeTo(ADXL345_DUR, _b);  
        // }

        // // Gets the DUR byte
        // public int getTapDuration() {
        //     byte _b;
        //     readFrom(ADXL345_DUR, 1, &_b);  
        //     return int (_b);
        // }

        // // Sets the latency (latent register) which contains an unsigned time value
        // // representing the wait time from the detection of a tap event to the start
        // // of the time window, during which a possible second tap can be detected.
        // // The scale factor is 1.25ms/LSB. A value of 0 disables the double tap function.
        // // It accepts a maximum value of 255.
        // public void setDoubleTapLatency(int doubleTapLatency) {
        //     byte _b = byte (doubleTapLatency);
        //     writeTo(ADXL345_LATENT, _b);  
        // }

        // // Gets the Latent value
        // public int getDoubleTapLatency() {
        //     byte _b;
        //     readFrom(ADXL345_LATENT, 1, &_b);  
        //     return int (_b);
        // }

        // // Sets the Window register, which contains an unsigned time value representing
        // // the amount of time after the expiration of the latency time (Latent register)
        // // during which a second valud tap can begin. The scale factor is 1.25ms/LSB. A
        // // value of 0 disables the double tap function. The maximum value is 255.
        // public void setDoubleTapWindow(int doubleTapWindow) {
        //     doubleTapWindow = constrain(doubleTapWindow,0,255);
        //     byte _b = byte (doubleTapWindow);
        //     writeTo(ADXL345_WINDOW, _b);  
        // }

        // // Gets the Window register
        // public int getDoubleTapWindow() {
        //     byte _b;
        //     readFrom(ADXL345_WINDOW, 1, &_b);  
        //     return int (_b);
        // }

        // // Sets the THRESH_ACT byte which holds the threshold value for detecting activity.
        // // The data format is unsigned, so the magnitude of the activity event is compared 
        // // with the value is compared with the value in the THRESH_ACT register. The scale
        // // factor is 62.5mg/LSB. A value of 0 may result in undesirable behavior if the 
        // // activity interrupt is enabled. The maximum value is 255.
        // public void setActivityThreshold(int activityThreshold) {
        //     activityThreshold = constrain(activityThreshold,0,255);
        //     byte _b = byte (activityThreshold);
        //     writeTo(ADXL345_THRESH_ACT, _b);  
        // }

        // // Gets the THRESH_ACT byte
        // public int getActivityThreshold() {
        //     byte _b;
        //     readFrom(ADXL345_THRESH_ACT, 1, &_b);  
        //     return int (_b);
        // }

        // // Sets the THRESH_INACT byte which holds the threshold value for detecting inactivity.
        // // The data format is unsigned, so the magnitude of the inactivity event is compared 
        // // with the value is compared with the value in the THRESH_INACT register. The scale
        // // factor is 62.5mg/LSB. A value of 0 may result in undesirable behavior if the 
        // // inactivity interrupt is enabled. The maximum value is 255.
        // public void setInactivityThreshold(int inactivityThreshold) {
        //     inactivityThreshold = constrain(inactivityThreshold,0,255);
        //     byte _b = byte (inactivityThreshold);
        //     writeTo(ADXL345_THRESH_INACT, _b);  
        // }

        // // Gets the THRESH_INACT byte
        // public int getInactivityThreshold() {
        //     byte _b;
        //     readFrom(ADXL345_THRESH_INACT, 1, &_b);  
        //     return int (_b);
        // }

        // // Sets the TIME_INACT register, which contains an unsigned time value representing the
        // // amount of time that acceleration must be less thant the value in the THRESH_INACT
        // // register for inactivity to be declared. The scale factor is 1sec/LSB. The value must
        // // be between 0 and 255.
        // public void setTimeInactivity(int timeInactivity) {
        //     timeInactivity = constrain(timeInactivity,0,255);
        //     byte _b = byte (timeInactivity);
        //     writeTo(ADXL345_TIME_INACT, _b);  
        // }

        // // Gets the TIME_INACT register
        // public int getTimeInactivity() {
        //     byte _b;
        //     readFrom(ADXL345_TIME_INACT, 1, &_b);  
        //     return int (_b);
        // }

        // // Sets the THRESH_FF register which holds the threshold value, in an unsigned format, for
        // // free-fall detection. The root-sum-square (RSS) value of all axes is calculated and
        // // compared whith the value in THRESH_FF to determine if a free-fall event occured. The 
        // // scale factor is 62.5mg/LSB. A value of 0 may result in undesirable behavior if the free-fall
        // // interrupt is enabled. The maximum value is 255.
        // public void setFreeFallThreshold(int freeFallThreshold) {
        //     freeFallThreshold = constrain(freeFallThreshold,0,255);
        //     byte _b = byte (freeFallThreshold);
        //     writeTo(ADXL345_THRESH_FF, _b);  
        // }

        // // Gets the THRESH_FF register.
        // public int getFreeFallThreshold() {
        //     byte _b;
        //     readFrom(ADXL345_THRESH_FF, 1, &_b);  
        //     return int (_b);
        // }

        // // Sets the TIME_FF register, which holds an unsigned time value representing the minimum
        // // time that the RSS value of all axes must be less than THRESH_FF to generate a free-fall 
        // // interrupt. The scale factor is 5ms/LSB. A value of 0 may result in undesirable behavior if
        // // the free-fall interrupt is enabled. The maximum value is 255.
        // public void setFreeFallDuration(int freeFallDuration) {
        //     freeFallDuration = constrain(freeFallDuration,0,255);  
        //     byte _b = byte (freeFallDuration);
        //     writeTo(ADXL345_TIME_FF, _b);  
        // }

        // // Gets the TIME_FF register.
        // public int getFreeFallDuration() {
        //     byte _b;
        //     readFrom(ADXL345_TIME_FF, 1, &_b);  
        //     return int (_b);
        // }

        // public bool isActivityXEnabled() {  
        //     return getRegisterBit(ADXL345_ACT_INACT_CTL, 6); 
        // }
        // public bool isActivityYEnabled() {  
        //     return getRegisterBit(ADXL345_ACT_INACT_CTL, 5); 
        // }
        // public bool isActivityZEnabled() {  
        //     return getRegisterBit(ADXL345_ACT_INACT_CTL, 4); 
        // }
        // public bool isInactivityXEnabled() {  
        //     return getRegisterBit(ADXL345_ACT_INACT_CTL, 2); 
        // }
        // public bool isInactivityYEnabled() {  
        //     return getRegisterBit(ADXL345_ACT_INACT_CTL, 1); 
        // }
        // public bool isInactivityZEnabled() {  
        //     return getRegisterBit(ADXL345_ACT_INACT_CTL, 0); 
        // }

        // public void setActivityX(bool state) {  
        //     setRegisterBit(ADXL345_ACT_INACT_CTL, 6, state); 
        // }
        // public void setActivityY(bool state) {  
        //     setRegisterBit(ADXL345_ACT_INACT_CTL, 5, state); 
        // }
        // public void setActivityZ(bool state) {  
        //     setRegisterBit(ADXL345_ACT_INACT_CTL, 4, state); 
        // }
        // public void setInactivityX(bool state) {  
        //     setRegisterBit(ADXL345_ACT_INACT_CTL, 2, state); 
        // }
        // public void setInactivityY(bool state) {  
        //     setRegisterBit(ADXL345_ACT_INACT_CTL, 1, state); 
        // }
        // public void setInactivityZ(bool state) {  
        //     setRegisterBit(ADXL345_ACT_INACT_CTL, 0, state); 
        // }

        // public bool isActivityAc() { 
        //     return getRegisterBit(ADXL345_ACT_INACT_CTL, 7); 
        // }
        // public bool isInactivityAc(){ 
        //     return getRegisterBit(ADXL345_ACT_INACT_CTL, 3); 
        // }

        // public void setActivityAc(bool state) {  
        //     setRegisterBit(ADXL345_ACT_INACT_CTL, 7, state); 
        // }
        // public void setInactivityAc(bool state) {  
        //     setRegisterBit(ADXL345_ACT_INACT_CTL, 3, state); 
        // }

        // public bool getSuppressBit(){ 
        //     return getRegisterBit(ADXL345_TAP_AXES, 3); 
        // }
        // public void setSuppressBit(bool state) {  
        //     setRegisterBit(ADXL345_TAP_AXES, 3, state); 
        // }

        // public bool isTapDetectionOnX(){ 
        //     return getRegisterBit(ADXL345_TAP_AXES, 2); 
        // }
        // public void setTapDetectionOnX(bool state) {  
        //     setRegisterBit(ADXL345_TAP_AXES, 2, state); 
        // }
        // public bool isTapDetectionOnY(){ 
        //     return getRegisterBit(ADXL345_TAP_AXES, 1); 
        // }
        // public void setTapDetectionOnY(bool state) {  
        //     setRegisterBit(ADXL345_TAP_AXES, 1, state); 
        // }
        // public bool isTapDetectionOnZ(){ 
        //     return getRegisterBit(ADXL345_TAP_AXES, 0); 
        // }
        // public void setTapDetectionOnZ(bool state) {  
        //     setRegisterBit(ADXL345_TAP_AXES, 0, state); 
        // }

        // public bool isActivitySourceOnX(){ 
        //     return getRegisterBit(ADXL345_ACT_TAP_STATUS, 6); 
        // }
        // public bool isActivitySourceOnY(){ 
        //     return getRegisterBit(ADXL345_ACT_TAP_STATUS, 5); 
        // }
        // public bool isActivitySourceOnZ(){ 
        //     return getRegisterBit(ADXL345_ACT_TAP_STATUS, 4); 
        // }

        // public bool isTapSourceOnX(){ 
        //     return getRegisterBit(ADXL345_ACT_TAP_STATUS, 2); 
        // }
        // public bool isTapSourceOnY(){ 
        //     return getRegisterBit(ADXL345_ACT_TAP_STATUS, 1); 
        // }
        // public bool isTapSourceOnZ(){ 
        //     return getRegisterBit(ADXL345_ACT_TAP_STATUS, 0); 
        // }

        // public bool isAsleep(){ 
        //     return getRegisterBit(ADXL345_ACT_TAP_STATUS, 3); 
        // }

        // public bool isLowPower(){ 
        //     return getRegisterBit(ADXL345_BW_RATE, 4); 
        // }
        // public void setLowPower(bool state) {  
        //     setRegisterBit(ADXL345_BW_RATE, 4, state); 
        // }

        // public double getRate(){
        //     byte _b;
        //     readFrom(ADXL345_BW_RATE, 1, &_b);
        //     _b &= B00001111;
        //     return (pow(2,((int) _b)-6)) * 6.25;
        // }

        // public void setRate(double rate){
        //     byte _b,_s;
        //     int v = (int) (rate / 6.25);
        //     int r = 0;
        //     while (v >>= 1)
        //     {
        //         r++;
        //     }
        //     if (r <= 9) { 
        //         readFrom(ADXL345_BW_RATE, 1, &_b);
        //         _s = (byte) (r + 6) | (_b & B11110000);
        //         writeTo(ADXL345_BW_RATE, _s);
        //     }
        // }

        // public void set_bw(byte bw_code){
        //     if((bw_code < ADXL345_BW_3) || (bw_code > ADXL345_BW_1600)){
        //         status = false;
        //         error_code = ADXL345_BAD_ARG;
        //     }
        //     else{
        //         writeTo(ADXL345_BW_RATE, bw_code);
        //     }
        // }

        // public byte get_bw_code(){
        //     byte bw_code;
        //     readFrom(ADXL345_BW_RATE, 1, &bw_code);
        //     return bw_code;
        // }





        // //Used to check if action was triggered in interrupts
        // //Example triggered(interrupts, ADXL345_SINGLE_TAP);
        // public bool triggered(byte interrupts, int mask){
        //     return ((interrupts >> mask) & 1);
        // }


        // /*
        //  ADXL345_DATA_READY
        //  ADXL345_SINGLE_TAP
        //  ADXL345_DOUBLE_TAP
        //  ADXL345_ACTIVITY
        //  ADXL345_INACTIVITY
        //  ADXL345_FREE_FALL
        //  ADXL345_WATERMARK
        //  ADXL345_OVERRUNY
        //  */





        // byte ADXL345::getInterruptSource() {
        //     byte _b;
        //     readFrom(ADXL345_INT_SOURCE, 1, &_b);
        //     return _b;
        // }

        // bool ADXL345::getInterruptSource(byte interruptBit) {
        //     return getRegisterBit(ADXL345_INT_SOURCE,interruptBit);
        // }

        // bool ADXL345::getInterruptMapping(byte interruptBit) {
        //     return getRegisterBit(ADXL345_INT_MAP,interruptBit);
        // }

        // // Set the mapping of an interrupt to pin1 or pin2
        // // eg: setInterruptMapping(ADXL345_INT_DOUBLE_TAP_BIT,ADXL345_INT2_PIN);
        // void ADXL345::setInterruptMapping(byte interruptBit, bool interruptPin) {
        //     setRegisterBit(ADXL345_INT_MAP, interruptBit, interruptPin);
        // }

        // bool ADXL345::isInterruptEnabled(byte interruptBit) {
        //     return getRegisterBit(ADXL345_INT_ENABLE,interruptBit);
        // }

        // void ADXL345::setInterrupt(byte interruptBit, bool state) {
        //     setRegisterBit(ADXL345_INT_ENABLE, interruptBit, state);
        // }

        // void ADXL345::setRegisterBit(byte regAdress, int bitPos, bool state) {
        //     byte _b;
        //     readFrom(regAdress, 1, &_b);
        //     if (state) {
        //         _b |= (1 << bitPos);  // forces nth bit of _b to be 1.  all other bits left alone.
        //     } 
        //     else {
        //         _b &= ~(1 << bitPos); // forces nth bit of _b to be 0.  all other bits left alone.
        //     }
        //     writeTo(regAdress, _b);  
        // }

        // bool ADXL345::getRegisterBit(byte regAdress, int bitPos) {
        //     byte _b;
        //     readFrom(regAdress, 1, &_b);
        //     return ((_b >> bitPos) & 1);
        // }

        // // print all register value to the serial ouptut, which requires it to be setup
        // // this can be used to manually to check the current configuration of the device
        // void ADXL345::printAllRegister() {
        //     byte _b;
        //     Serial.print("0x00: ");
        //     readFrom(0x00, 1, &_b);
        //     print_byte(_b);
        //     Serial.println("");
        //     int i;
        //     for (i=29;i<=57;i++){
        //         Serial.print("0x");
        //         Serial.print(i, HEX);
        //         Serial.print(": ");
        //         readFrom(i, 1, &_b);
        //         print_byte(_b);
        //         Serial.println("");    
        //     }
        // }

        // void print_byte(byte val){
        //     int i;
        //     Serial.print("B");
        //     for(i=7; i>=0; i--){
        //         Serial.print(val >> i & 1, BIN);
        //     }
        // }
    }
}

namespace configuration
{
    public enum AccelerationAxes : byte
    {
        None = 0,
        X = 0,
        Y = 0,
        Z = 0 
    }
}

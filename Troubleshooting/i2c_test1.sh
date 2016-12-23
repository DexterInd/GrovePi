#! /bin/bash
echo ""
echo Checking I2C bus for devices
echo ============================
echo ""

# insert a wait here to make sure the ATMEGA is reset and ready
sleep 1
echo Checking I2C bus 0
echo ==================
i2cdetect -y 0 

echo ""
echo Checking I2C bus 1
echo ==================
i2cdetect -y 1 

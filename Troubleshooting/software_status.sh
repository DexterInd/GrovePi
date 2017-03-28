#! /bin/bash
#echo Checking for dependencies 
#echo troubleshooting_script_v1 #> error_log.txt
echo ""
echo Check space left #>> error_log.txt
echo ================ #>>error_log.txt
df -h

echo ""
echo Check for dependencies #>> error_log.txt
echo ======================
dpkg-query -W -f='${Package} ${Version} ${Status}\n' python #>> error_log.txt
dpkg-query -W -f='${Package} ${Version} ${Status}\n' python-pip #>> error_log.txt
dpkg-query -W -f='${Package} ${Version} ${Status}\n' git #>> error_log.txt
dpkg-query -W -f='${Package} ${Version} ${Status}\n' libi2c-dev #>> error_log.txt
dpkg-query -W -f='${Package} ${Version} ${Status}\n' python-serial #>> error_log.txt
dpkg-query -W -f='${Package} ${Version} ${Status}\n' python-rpi.gpio #>> error_log.txt
dpkg-query -W -f='${Package} ${Version} ${Status}\n' i2c-tools #>> error_log.txt
dpkg-query -W -f='${Package} ${Version} ${Status}\n' python-smbus #>> error_log.txt
dpkg-query -W -f='${Package} ${Version} ${Status}\n' arduino #>> error_log.txt
dpkg-query -W -f='${Package} ${Version} ${Status}\n' minicom #>> error_log.txt
dpkg-query -W -f='${Package} ${Version} ${Status}\n' scratch #>> error_log.txt
echo "" #>>error_log.txt

#Check for wiringPi
if [[ -n $(find / -name 'wiringPi') ]]
then
  echo "wiringPi Found" #>>error_log.txt
else
  echo "wiringPi Not Found (ERR)" #>>error_log.txt
fi

if [[ -n $(find / -name 'wiringPi') ]]
then
  echo "wiringPi Found" #>>error_log.txt
else
  echo "wiringPi Not Found (ERR)"#>>error_log.txt
fi

#Check for changes in blacklist
if grep -q "#blacklist i2c-bcm2708" /etc/modprobe.d/raspi-blacklist.conf; then
	echo "I2C already removed from blacklist" #>>error_log.txt
else
	echo "I2C still in blacklist (ERR)" #>>error_log.txt
fi

if grep -q "#blacklist spi-bcm2708" /etc/modprobe.d/raspi-blacklist.conf; then
	echo "SPI already removed from blacklist" #>>error_log.txt
else
	echo "SPI still in blacklist (ERR)" #>>error_log.txt
fi
echo "" #>>error_log.txt

echo ""
echo Check for addition in /modules #>>error_log.txt
echo ============================== #>>error_log.txt
if grep -q "i2c-dev" /etc/modules; then
	echo "I2C-dev already there" #>>error_log.txt
else
	echo "I2C-dev not there (ERR)" #>>error_log.txt
fi
if grep -q "i2c-bcm2708" /etc/modules; then
	echo "i2c-bcm2708 already there" #>>error_log.txt
else
	echo "i2c-bcm2708 not there (ERR)" #>>error_log.txt
fi
if grep -q "spi-dev" /etc/modules; then
	echo "spi-dev already there" #>>error_log.txt
else
	echo "spi-dev not there (ERR)" #>>error_log.txt
fi
echo "" #>>error_log.txt

echo ""
#echo Checking Hardware revision 
echo Hardware revision #>>error_log.txt
echo ================= #>>error_log.txt
gpio -v #>>error_log.txt
echo "" #>>error_log.txt

echo ""
#echo Check the /dev folder
echo Check the /dev folder #>>error_log.txt
echo ===================== #>>error_log.txt
ls /dev | grep 'i2c' #>>error_log.txt
ls /dev | grep 'spi' #>>error_log.txt
ls /dev | grep 'ttyAMA' #>>error_log.txt
echo "" #>>error_log.txt

echo "USB device status"
echo =================
lsusb
echo ""
lsusb -t

echo "Raspbian for Robots Version"
echo ===========================
cat /home/pi/di_update/Raspbian_For_Robots/Version
echo ""
echo ""

echo "Hostname"
echo ========
cat /etc/hostname
echo ""
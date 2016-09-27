#!/usr/bin/env bash
echo "  _____            _                                ";
echo " |  __ \          | |                               ";
echo " | |  | | _____  _| |_ ___ _ __                     ";
echo " | |  | |/ _ \ \/ / __/ _ \ '__|                    ";
echo " | |__| |  __/>  <| ||  __/ |                       ";
echo " |_____/ \___/_/\_\\__\___|_| _        _            ";
echo " |_   _|         | |         | |      (_)           ";
echo "   | |  _ __   __| |_   _ ___| |_ _ __ _  ___  ___  ";
echo "   | | | '_ \ / _\` | | | / __| __| '__| |/ _ \/ __|";
echo "  _| |_| | | | (_| | |_| \__ \ |_| |  | |  __/\__ \ ";
echo " |_____|_| |_|\__,_|\__,_|___/\__|_|  |_|\___||___/ ";
echo "                                                    ";
echo "                                                    ";
echo " "
printf "WELCOME TO IR RECEIVER SETUP FOR THE GOPIGO.\nPlease ensure internet connectivity before running this script.\nNOTE: Reboot Raspberry Pi after completion.\n"

echo " "
echo "Check for internet connectivity..."
echo "=================================="
wget -q --tries=2 --timeout=20 --output-document=/dev/null http://raspberrypi.org
if [ $? -eq 0 ];then
	echo "Connected"
else
	echo "Unable to Connect, try again !!!"
	exit 0
fi

echo " "
echo "Installing Dependencies"
echo "======================="
sudo apt-get update
sudo apt-get install lirc python-lirc

echo " "
echo "Copying Config Files"
echo "===================="
sudo cp hardware_copy.conf /etc/lirc/hardware.conf
sudo cp lircd_keyes.conf /etc/lirc/lircd.conf
sudo cp lircrc_keyes /etc/lirc/lircrc
echo "Files copied"

echo " "
echo "Enabling LIRC"
echo "======================="

if grep -q "lirc_dev" /etc/modules; then
	echo "Lib dev already present"
else
	sudo echo "lirc_dev" >> /etc/modules
	echo "Lib dev added"
fi


echo "Check Lib Rpi GPIO"
if grep -q "lirc_rpi gpio_in_pin=14" /etc/modules; then
	echo "Lib Rpi GPIO already present"

echo "Check Pin 15"
elif grep -q "lirc_rpi gpio_in_pin=15" /etc/modules; then
	sed -e s/"lirc_rpi gpio_in_pin=15"//g -i /etc/modules
	sudo echo "lirc_rpi gpio_in_pin=14" >> /etc/modules
	echo "Lib Rpi GPIO changed from pin 15 to 14"
	
else
	sudo echo "lirc_rpi gpio_in_pin=14" >> /etc/modules
	echo "Lib Rpi GPIO added"
fi

echo "Check Kernel Version."
if grep -q "dtoverlay=lirc-rpi,gpio_in_pin=14" /boot/config.txt; then
	echo "LIRC for Kernel 3.18 already present"
echo "Check Kernel pin 15"
	elif grep -q "dtoverlay=lirc-rpi,gpio_in_pin=15" /boot/config.txt; then
	sed -e s/"dtoverlay=lirc-rpi,gpio_in_pin=15"//g -i /boot/config.txt
	sudo echo "dtoverlay=lirc-rpi,gpio_in_pin=14" >> /boot/config.txt
	echo "LIRC for Kernel 3.18 changed from pin 15 to 14"
	
else
	sudo echo "dtoverlay=lirc-rpi,gpio_in_pin=14" >> /boot/config.txt
	echo "LIRC for Kernel 3.18 added"
fi



echo " "
echo "Please restart the Raspberry Pi for the changes to take effect"
echo "  _____  ______  _____ _______       _____ _______ "
echo " |  __ \|  ____|/ ____|__   __|/\   |  __ \__   __|"
echo " | |__) | |__  | (___    | |  /  \  | |__) | | |   "
echo " |  _  /|  __|  \___ \   | | / /\ \ |  _  /  | |   "
echo " | | \ \| |____ ____) |  | |/ ____ \| | \ \  | |   "
echo " |_|  \_\______|_____/   |_/_/    \_\_|  \_\ |_|   "
echo " "
echo "To Restart type 'sudo reboot'"

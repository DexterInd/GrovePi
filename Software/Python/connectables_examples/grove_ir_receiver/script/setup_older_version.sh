#!/usr/bin/env bash
if grep -q "lirc_rpi gpio_in_pin=15" /etc/modules; then
	echo "Lib Rpi GPIO already present"
	
elif grep -q "lirc_rpi gpio_in_pin=14" /etc/modules; then
	sed -e s/"lirc_rpi gpio_in_pin=14"//g -i /etc/modules
	sudo echo "lirc_rpi gpio_in_pin=15" >> /etc/modules
	echo "Lib Rpi GPIO changed from pin 14 to 15"
	
else
	sudo echo "lirc_rpi gpio_in_pin=15" >> /etc/modules
	echo "Lib Rpi GPIO added"
fi

if grep -q "dtoverlay=lirc-rpi,gpio_in_pin=15" /boot/config.txt; then
	echo "LIRC for Kernel 3.18 already present"
	
elif grep -q "dtoverlay=lirc-rpi,gpio_in_pin=14" /boot/config.txt; then
	sed -e s/"dtoverlay=lirc-rpi,gpio_in_pin=14"//g -i /boot/config.txt
	sudo echo "dtoverlay=lirc-rpi,gpio_in_pin=15" >> /boot/config.txt
	echo "LIRC for Kernel 3.18 changed from pin 14 to 15"
	
else
	sudo echo "dtoverlay=lirc-rpi,gpio_in_pin=15" >> /boot/config.txt
	echo "LIRC for Kernel 3.18 added"
fi

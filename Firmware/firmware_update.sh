#! /bin/bash
echo "Updating the GrovePi firmware"
echo "============================="
echo " "
echo " Run this program: "
echo " sudo ./firmware_update.sh"
echo " "
echo "============================="

read -n1 -p "Do you want to update the firmware? [y,n]" input
if [[ $input == "Y" || $input == "y" ]]; then
       	printf "\nMake sure that GrovePi is connected to Raspberry Pi"
else
        printf "\nExiting..."
	exit 0
fi
if [ $(find $pwd -name "grove_pi_firmware.hex") ]; then 
	printf "\nFirmware found"
else
	printf "\nFirmware not found\nCheck if firmware is there or run again\nPress any key to exit"
 	read
	exit 0
fi

printf "\nPress any key to start firmware update\n. . .";
read -n1
avrdude -c gpio -p m328p -U lfuse:w:0xFF:m
avrdude -c gpio -p m328p -U hfuse:w:0xDA:m
avrdude -c gpio -p m328p -U efuse:w:0x05:m
avrdude -c gpio -p m328p -U flash:w:grove_pi_firmware.hex



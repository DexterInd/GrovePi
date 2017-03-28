#! /bin/bash
echo "Updating the GrovePi firmware to 1.2.7(experimental)"
echo "===================================================="
echo " http://www.dexterindustries.com/grovepi "
echo " Run this program: "
echo " sudo ./firmware_update_1_2_7.sh"
echo " "
echo "===================================================="
echo " If you find problems with the beta firmware, use the stable firmware update from here https://github.com/DexterInd/GrovePi/tree/master/Firmware "
echo "===================================================="

read -n1 -p "Do you want to update the firmware? [y,n]" input
if [[ $input == "Y" || $input == "y" ]]; then
       	printf "\nMake sure that GrovePi is connected to Raspberry Pi"
else
        printf "\nExiting..."
	exit 0
fi
if [ $(find $pwd -name "grove_pi_v1_2_7.cpp.hex") ]; then 
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
avrdude -c gpio -p m328p -U flash:w:grove_pi_v1_2_7.cpp.hex
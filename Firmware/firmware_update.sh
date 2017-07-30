#! /bin/bash
REPO_PATH=$(readlink -f $(dirname $0) | grep -E -o "^(.*?\\GrovePi)")
echo "Updating the GrovePi firmware"
echo "============================="
echo " http://www.dexterindustries.com/grovepi "
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
source $REPO_PATH/Firmware/grovepi_firmware_update.sh
update_grovepi_firmware

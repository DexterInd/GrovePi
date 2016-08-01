#! /bin/bash
echo "Updating the GrovePi firmware and software with the Experimntal software and firmware"
echo "====================================================================================="
echo " http://www.dexterindustries.com/grovepi "
echo "========================================="

read -n1 -p "Do you want to update the firmware? [y,n]" input
if [[ $input == "Y" || $input == "y" ]]; then
       	printf "\nMake sure that GrovePi is connected to Raspberry Pi"
else
        printf "\nExiting..."
	exit 0
fi

printf "\nPress any key to start firmware update\n. . .";
read -n1
sudo avrdude -c gpio -p m328p -U flash:w:grove_pi_v1_2_6.cpp.hex
printf "\nUpdating GrovePi.py\n. . .";
sudo cp grovepi.py ../../../../Software/Python/
sudo python ../../../../Software/Python/setup.py install
printf "\nChecking Firmware Version (should be 1.2.6)\n. . .\n";
sudo python ../../../../Software/Python/grove_firmware_version_check.py
#! /bin/bash
echo "Updating the GrovePi firmware"
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
	echo "=================="
else
	printf "\nFirmware not found\nCheck if firmware is there or run again\nPress any key to exit"
 	read
	exit 0
fi

printf "\nDo you want to do I2C search for GrovePi or do you want to directly update the firmware?\n(I2C search recommended\nPress Y for I2C Search or N for direct upload [y,n]"
read -n1 input
if [[ $input == "Y" || $input == "y" ]]; then
        #Revision in /proc/cpuinfo 
	#	0002 or 0003    : Rev1
	#	else		: Rev2	
	rev=$(grep Rev /proc/cpuinfo)
	if [[ $rev  == *0002* ]];then
		dev=$(i2cdetect -y 0 04 04)
	elif [[ $rev  == *0003* ]];then
		dev=$(i2cdetect -y 0 04 04)
	else
		dev=$(i2cdetect -y 1 04 04)
	fi
	printf "\n=================================================="
	if [[ $dev  == *04* ]];then
	  	printf "\nGrovePi Found. Connect the jumper to the Reset pin and Press any key to start firmware update\n. . .";
		read -n1
	else
		printf "\nGrovePi Not Found"
		read
		exit 0
	fi
	avrdude -c gpio -p m328p -U flash:w:grove_pi_firmware.hex
else
  	printf "\nConnect the jumper to the Reset pin and Press any key to start firmware update\n. . .";
	read -n1
	avrdude -c gpio -p m328p -U flash:w:grove_pi_firmware.hex
fi


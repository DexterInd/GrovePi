#! /bin/bash
printf "Welcome to GrovePi Firmware Update Check.\n=========================================\nPlease ensure internet connectivity before running this script.\n"
echo "Must be running as Root user"
echo "Press any key to begin..."
read

echo "Check for internet connectivity..."
echo "=================================="
wget -q --tries=2 --timeout=20 http://google.com
if [[ $? -eq 0 ]];then
	echo "Connected"
else
	echo "Unable to Connect, try again !!!"
	exit 0
fi

wget https://raw.github.com/DexterInd/GrovePi/master/Firmware/version.txt -O temp_f &>/dev/null
diff -q version.txt temp_f
if [[ $? == "0" ]]
then
  echo "You have the latest firmware"
else
  printf "\nNew firmware available. \n\nDownload the new version from Dexter Industries Github Repo and follow the update guide on the GrovePi Homepage to update the firmware.\n"  
fi
rm temp_f